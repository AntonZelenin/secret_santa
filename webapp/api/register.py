from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action

from tools import helpers
from webapp import email as em


@csrf_exempt
@action(detail=True, methods=['POST'])
def email(request: HttpRequest) -> HttpResponse:
    json_data = helpers.load_json(request)
    email_ = json_data['email']

    # todo check if the user is already registered
    try:
        validate_email(email_)
    except ValidationError as e:
        return HttpResponse(e.messages, status=400)

    try:
        em.registration_manager.register_email(email_)
    except em.registration_manager.EmailRegistrationException as e:
        return HttpResponse(e, status=500)

    return HttpResponse()

## what about dos attacks? how to prevent sending spam to random emails? by ip?
## minimum time between sending subsequent email with code, expiration time of a code
# post send code again:
## get email, validate it, check minimum waiting time, generate code, send email, response with a success/error message
# post register via google
# post login: get email, get password, validate it, generate token, response with.. something
