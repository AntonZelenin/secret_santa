from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from tools import helpers
from tools.types import ErrJsonResponse
from webapp import serializers, password_manager


# todo why csrf_exempt, remove?
@csrf_exempt
@require_POST
def request_password_reset(request: HttpRequest) -> HttpResponse:
    res = serializers.password.RequestPasswordResetSerializer(data=helpers.load_json(request))

    if res.is_valid():
        email = res.validated_data['email']
    else:
        return ErrJsonResponse(res.errors, status=400)

    # todo error handling
    password_manager.request_password_reset(email)


@csrf_exempt
@require_POST
def reset_password(request: HttpRequest) -> HttpResponse:
    res = serializers.password.SetPasswordSerializer(data=helpers.load_json(request))

    if not res.is_valid():
        return ErrJsonResponse(res.errors, status=400)

    user_id = res.validated_data['user_id']
    password = res.validated_data['password']
    # todo error handling
    password_manager.set_password(user_id, password)
