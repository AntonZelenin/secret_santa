from datetime import timedelta, datetime

from django.contrib.auth.models import User
from django.db import IntegrityError

import tools.helpers
from webapp.registration.verification import VerificationEmailSendingException
from webapp.models import TmpUser, EmailVerificationCode
from webapp import registration


def register_email(email: str):
    if _is_user_already_registered(email):
        # todo what should be the error message?
        raise EmailRegistrationException(
            'This email is already registered. Please use a different email address or sign in'
        )

    try:
        code = EmailVerificationCode.objects.get(email=email)
        if code.resend_at < datetime.now():
            code.delete()
            TmpUser.objects.get(email=email).delete()
        else:
            # todo what should be the error message?
            raise EmailRegistrationException('Please try in a minute')
    except (EmailVerificationCode.DoesNotExist, TmpUser.DoesNotExist):
        pass

    now = datetime.now()
    try:
        user = TmpUser.objects.create(email=email, created_at=now)
    except IntegrityError:
        raise EmailRegistrationException('Failed to create a user')

    code = tools.helpers.generate_6_digit_code()
    resend_at = now + _get_code_resend_delta()
    expires_at = now + _get_code_expiration_delta()
    try:
        code_obj = EmailVerificationCode.objects.create(
            code=code, email=email, created_at=now, resend_at=resend_at, expires_at=expires_at,
        )
    except IntegrityError:
        user.delete()
        # todo users should no get such a message
        raise EmailRegistrationException('Failed to save the verification code')

    try:
        registration.verification.send_verification_code(email, 'some random code')
    except VerificationEmailSendingException as e:
        user.delete()
        code_obj.delete()
        raise EmailRegistrationException(e)
    except Exception as e:
        raise EmailRegistrationException(e)


def is_code_valid(email: str, code: str) -> bool:
    # todo prevent brute force attacks
    try:
        TmpUser.objects.get(email=email)
        code_obj = EmailVerificationCode.objects.get(email=email)
        if code_obj.code == code:
            if code_obj.expires_at > datetime.now():
                return True
            else:
                # todo you should send the correct error code
                raise EmailRegistrationException('Code expired')
        else:
            return False
    except (EmailVerificationCode.DoesNotExist, TmpUser.DoesNotExist):
        return False


def mark_email_as_verified(email: str):
    user = TmpUser.objects.get(email=email)
    user.email_verified = True
    user.save()


def set_password(email: str, password: str):
    user = TmpUser.objects.get(email=email)
    user.password = password
    user.save()


def _is_user_already_registered(email: str) -> bool:
    try:
        User.objects.get(email=email)
        return True
    except User.DoesNotExist:
        return False


def _get_code_resend_delta() -> timedelta:
    return timedelta(minutes=1)


def _get_code_expiration_delta() -> timedelta:
    # todo what should be the expiration time?
    return timedelta(minutes=3)


class EmailRegistrationException(Exception):
    pass
