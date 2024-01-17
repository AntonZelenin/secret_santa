from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from tools import helpers
from tools.types import Ok, Err, ErrJsonResponse
from webapp import registration, repository
from webapp.models import User, SetUsernameToken


# todo why csrf_exempt, remove?
@csrf_exempt
@require_POST
def email(request: HttpRequest) -> HttpResponse:
    """
    Creates a tmp user with an email and sends a verification code to the email
    """

    json_data = helpers.load_json(request)
    email_ = json_data['email']

    try:
        validate_email(email_)
    except ValidationError as e:
        return ErrJsonResponse(e.messages, status=400)

    try:
        registration.manager.create_user(email_)
    except registration.manager.EmailRegistrationException as e:
        return ErrJsonResponse(str(e), status=400)

    return HttpResponse(status=200)


@csrf_exempt
@require_POST
def verify_email(request: HttpRequest) -> JsonResponse:
    json_data = helpers.load_json(request)
    email_ = json_data['email']
    code = json_data['verification_code']

    match registration.manager.check_code(email_, code):
        case Ok():
            registration.manager.delete_email_verification_code(email_)
            registration.manager.mark_email_as_verified(email_)

            return JsonResponse({
                'create_password_token': default_token_generator.make_token(User.objects.get(email=email_)),
            })
        case Err(error):
            return ErrJsonResponse(error, status=400)


@require_POST
def resend_email_verification_code(request: HttpRequest) -> HttpResponse:
    json_data = helpers.load_json(request)
    email_ = json_data['email']

    try:
        registration.manager.create_user(email_)
    except registration.manager.EmailRegistrationException as e:
        return ErrJsonResponse(str(e), status=400)

    return HttpResponse(status=200)


@csrf_exempt
@require_POST
def password(request: HttpRequest) -> JsonResponse:
    json_data = helpers.load_json(request)
    email_ = json_data['email']
    password_ = json_data['password']
    create_password_token = json_data['create_password_token']
    user = repository.get_user_by_email(email_)

    if user is None:
        return ErrJsonResponse('Invalid email', status=400)

    if not default_token_generator.check_token(user, create_password_token):
        # todo what is a good message?
        return ErrJsonResponse('Invalid password reset token', status=400)

    # todo it doesn't hash the password!
    registration.manager.set_password(email_, password_)

    return JsonResponse({
        'create_username_token': registration.manager.create_set_username_token(email_).token,
    })


@csrf_exempt
@require_POST
def username(request: HttpRequest) -> HttpResponse:
    json_data = helpers.load_json(request)
    email_ = json_data['email']
    username_ = json_data['username']
    create_username_token = json_data['create_username_token']
    user = User.objects.get(email=email_)
    set_username_token = SetUsernameToken.objects.get(user=user)

    if create_username_token == set_username_token.token:
        set_username_token.delete()
    else:
        # todo what is a good message?
        return ErrJsonResponse('Invalid create_username_token', status=400)

    user.username = username_
    user.finished_registration = True
    user.save()

    return HttpResponse(status=200)

## what about dos attacks? how to prevent sending spam to random emails? by ip?
## minimum time between sending subsequent registration with code, expiration time of a code
# post send code again:
## get registration, validate it, check minimum waiting time, generate code, send registration, response with a success/error message
# post register via google
# post login: get registration, get password, validate it, generate token, response with.. something
