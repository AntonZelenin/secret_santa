from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action

from tools import helpers
from webapp import registration as em
from webapp.models import TmpUser


# todo remove csrf_exempt
@csrf_exempt
@action(detail=True, methods=['POST'])
def email(request: HttpRequest) -> HttpResponse:
    json_data = helpers.load_json(request)
    email_ = json_data['registration']

    try:
        validate_email(email_)
    except ValidationError as e:
        return HttpResponse(e.messages, status=400)

    try:
        em.registration_manager.register_email(email_)
    except em.registration_manager.EmailRegistrationException as e:
        return HttpResponse(e, status=500)

    return HttpResponse()


@action(detail=True, methods=['POST'])
def verify_email(request: HttpRequest) -> HttpResponse:
    json_data = helpers.load_json(request)
    email_ = json_data['registration']
    code = json_data['code']

    if em.registration_manager.is_code_valid(email_, code):
        em.registration_manager.mark_email_as_verified(email_)
        user = TmpUser.objects.get(email=email_)
        body = {
            'create_password_token': default_token_generator.make_token(user),
        }
        return HttpResponse(body)
    else:
        return HttpResponse('Invalid code', status=400)


@action(detail=True, methods=['POST'])
def resend_email_verification_code(request: HttpRequest) -> HttpResponse:
    json_data = helpers.load_json(request)
    email_ = json_data['registration']

    try:
        em.registration_manager.register_email(email_)
    except em.registration_manager.EmailRegistrationException as e:
        return HttpResponse(e, status=500)

    return HttpResponse()


@action(detail=True, methods=['POST'])
def password(request: HttpRequest) -> HttpResponse:
    json_data = helpers.load_json(request)
    email_ = json_data['registration']
    password_ = json_data['password']
    create_password_token = json_data['create_password_token']
    user = TmpUser.objects.get(email=email_)

    if not default_token_generator.check_token(user.id, create_password_token):
        # todo what is a good message?
        return HttpResponse('Invalid password reset token', status=400)

    em.registration_manager.set_password(email_, password_)

    # todo what if user left without setting the name? it will loose the token
    # todo redirect to registration? I think yes, unfinished registration is not valid
    return HttpResponse({
        'create_username_token': default_token_generator.make_token(user),
    })


@action(detail=True, methods=['POST'])
def username(request: HttpRequest) -> HttpResponse:
    json_data = helpers.load_json(request)
    email_ = json_data['registration']
    username_ = json_data['username']
    create_username_token = json_data['create_username_token']
    user = TmpUser.objects.get(email=email_)

    if not default_token_generator.check_token(user.id, create_username_token):
        # todo what is a good message?
        return HttpResponse('Invalid username reset token', status=400)

    user.username = username_
    user.save()

    return HttpResponse()


## what about dos attacks? how to prevent sending spam to random emails? by ip?
## minimum time between sending subsequent registration with code, expiration time of a code
# post send code again:
## get registration, validate it, check minimum waiting time, generate code, send registration, response with a success/error message
# post register via google
# post login: get registration, get password, validate it, generate token, response with.. something
