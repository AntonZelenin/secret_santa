from datetime import timedelta, datetime

from django.contrib.auth.models import User
from django.db import IntegrityError

import tools.helpers
from webapp.email.verification import VerificationEmailSendingException
from webapp.models import TmpUser, EmailVerificationCode
from webapp import email as em


def register_email(email: str):
    if _is_user_already_registered(email):
        # todo what should be the error message?
        raise EmailRegistrationException(
            'This email is already registered. Please use a different email address or try to recover your account'
        )

    try:
        code = EmailVerificationCode.objects.get(email=email)
        if code.expires_at < datetime.now():
            code.delete()
            TmpUser.objects.get(email=email).delete()
        else:
            # todo what should be the error message?
            raise EmailRegistrationException(
                'This email is already registered. Please use a different email address, please try again in a minute'
            )
    except (EmailVerificationCode.DoesNotExist, TmpUser.DoesNotExist):
        pass

    now = datetime.now()
    try:
        user = TmpUser.objects.create(email=email, created_at=now)
    except IntegrityError:
        raise EmailRegistrationException('Failed to create a user')

    code = tools.helpers.generate_6_digit_code()
    expires_at = now + _get_code_expiration_delta()
    try:
        code_obj = EmailVerificationCode.objects.create(code=code, email=email, created_at=now, expires_at=expires_at)
    except IntegrityError:
        user.delete()
        # todo users should no get such a message
        raise EmailRegistrationException('Failed to save the verification code')

    try:
        em.verification.send_verification_code(email, 'some random code')
    except VerificationEmailSendingException as e:
        user.delete()
        code_obj.delete()
        raise EmailRegistrationException(e)
    except Exception as e:
        raise EmailRegistrationException(e)


def _is_user_already_registered(email: str) -> bool:
    try:
        User.objects.get(email=email)
        return True
    except User.DoesNotExist:
        return False


def _get_code_expiration_delta() -> timedelta:
    return timedelta(minutes=1)


class EmailRegistrationException(Exception):
    pass
