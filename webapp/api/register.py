from django.http import HttpRequest, JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from tools import helpers, logger
from tools.types import Ok, Err, ErrJsonResponse
from webapp import registration, repository, serializers as srl, password_manager
from webapp.models import User, SetUsernameToken
from webapp.registration.manager import EmailRegistrationException, VerificationCodeException


# todo why csrf_exempt, remove?
@csrf_exempt
@require_POST
def email(request: HttpRequest) -> HttpResponse:
    """
    Creates a tmp user with an email and sends a verification code to the email
    """
    current_step = registration.constants.REGISTER_EMAIL

    res = srl.registration.EmailSerializer(data=helpers.load_json(request))
    if res.is_valid():
        email_ = res.validated_data['email']
    else:
        return ErrJsonResponse(res.errors, status=400)

    try:
        user = registration.manager.create_user(email_)
    except (EmailRegistrationException, VerificationCodeException) as e:
        return ErrJsonResponse(str(e), status=400)

    return JsonResponse({
        'user_id': user.id,
        'next_step': registration.manager.get_next_step(current_step),
    })


@csrf_exempt
@require_POST
def verify_email(request: HttpRequest) -> JsonResponse:
    current_step = registration.constants.VERIFY_EMAIL

    res = srl.registration.EmailVerificationCodeSerializer(data=helpers.load_json(request))
    if not res.is_valid():
        return ErrJsonResponse(res.errors, status=400)

    user_id = res.validated_data['user_id']
    code = res.validated_data['verification_code']
    match registration.manager.check_code(user_id, code):
        case Ok():
            registration.manager.delete_email_verification_code(user_id)
            registration.manager.mark_email_as_verified(user_id)

            return JsonResponse({
                'user_id': user_id,
                'set_password_token': password_manager.generate_password_reset_token(user_id),
                'next_step': registration.manager.get_next_step(current_step),
            })
        case Err(error):
            return ErrJsonResponse({'verification_code': error}, status=400)


@csrf_exempt
@require_POST
def resend_email_verification_code(request: HttpRequest) -> HttpResponse:
    current_step = registration.constants.RESEND_VERIFICATION_CODE

    res = srl.registration.ResendEmailVerificationCodeSerializer(data=helpers.load_json(request))
    if res.is_valid():
        user_id = res.validated_data['user_id']
    else:
        return ErrJsonResponse(res.errors, status=400)

    try:
        registration.manager.resend_verification_code(user_id)
    except (EmailRegistrationException, VerificationCodeException) as e:
        return ErrJsonResponse({'verification_code': str(e)}, status=400)

    return JsonResponse({
        'user_id': user_id,
        'next_step': registration.manager.get_next_step(current_step),
    })


@csrf_exempt
@require_POST
def password(request: HttpRequest) -> JsonResponse:
    current_step = registration.constants.CREATE_PASSWORD

    res = srl.password.SetPasswordSerializer(data=helpers.load_json(request))
    if not res.is_valid():
        return ErrJsonResponse(res.errors, status=400)

    user_id = res.validated_data['user_id']
    password_ = res.validated_data['password']
    set_password_token = res.validated_data['set_password_token']
    
    if not repository.user_exists(user_id):
        return ErrJsonResponse({'user_id': 'Invalid user_id'}, status=400)

    if not password_manager.check_password_reset_token(user_id, set_password_token):
        # todo what is a good message?
        return ErrJsonResponse({'password_token': 'Invalid password reset token'}, status=400)

    password_manager.set_password(user_id, password_)

    return JsonResponse({
        'user_id': user_id,
        'create_username_token': registration.manager.create_set_username_token(user_id).token,
        'next_step': registration.manager.get_next_step(current_step),
    })


@csrf_exempt
@require_POST
def username(request: HttpRequest) -> HttpResponse:
    current_step = registration.constants.CREATE_USERNAME

    res = srl.registration.CreateUsernameSerializer(data=helpers.load_json(request))
    if not res.is_valid():
        return ErrJsonResponse(res.errors, status=400)

    user_id = res.validated_data['user_id']
    username_ = res.validated_data['username']
    create_username_token = res.validated_data['create_username_token']
    user = User.objects.get(id=user_id)
    set_username_token = SetUsernameToken.objects.get(user=user)

    if create_username_token == set_username_token.token:
        set_username_token.delete()
    else:
        # todo what is a good message?
        return ErrJsonResponse({'username_token': 'Invalid create_username_token'}, status=400)

    user.nickname = username_
    user.finished_registration = True
    user.save()

    return JsonResponse({
        'user_id': user.id,
        'next_step': registration.manager.get_next_step(current_step),
    })
