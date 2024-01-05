from datetime import timedelta, datetime, timezone
from typing import Optional

from django.contrib.auth.models import User

import tools.helpers
from tools.types import Result, Ok, Err
from webapp.models import TmpUser, EmailVerificationCode
from webapp import registration


def register_email(email: str):
    if _is_user_already_registered(email):
        # todo what should be the error message?
        raise EmailRegistrationException(
            'This email is already registered. Please use a different email address or sign in'
        )

    existing_code = _get_existing_code(email)
    if existing_code:
        if existing_code.resend_at < datetime.now(timezone.utc):
            _clean_code_and_user(email, existing_code)
        else:
            # todo what should be the error message?
            raise EmailRegistrationException('Please try in a minute')

    now = datetime.now(timezone.utc)
    user = TmpUser.objects.create(email=email, created_at=now)
    code = tools.helpers.generate_6_digit_code()
    resend_at = now + _get_code_resend_delta()
    expires_at = now + _get_code_expiration_delta()

    try:
        verification_code = EmailVerificationCode.objects.create(
            code=code, email=email, created_at=now, resend_at=resend_at, expires_at=expires_at,
        )
    except Exception:
        user.delete()
        # todo users should no get such a message
        raise EmailRegistrationException('Failed to save the verification code')

    try:
        registration.verification.send_verification_code(email, 'some random code')
    except Exception as e:
        user.delete()
        verification_code.delete()
        raise EmailRegistrationException(e)


def check_code(email: str, code: str) -> Result[bool]:
    # todo prevent brute force attacks
    try:
        TmpUser.objects.get(email=email)
        code_obj = EmailVerificationCode.objects.get(email=email)
        if code_obj.code == code:
            if code_obj.expires_at > datetime.now(timezone.utc):
                return Ok()
            else:
                Err('The code is expired')
        else:
            return Err('Code has expired')
    except (EmailVerificationCode.DoesNotExist, TmpUser.DoesNotExist):
        return Err('Invalid code')


def mark_email_as_verified(email: str):
    user = TmpUser.objects.get(email=email)
    user.email_verified = True
    user.save()


def set_password(email: str, password: str):
    user = TmpUser.objects.get(email=email)
    user.password = password
    user.save()


def _get_existing_code(email: str) -> Optional[EmailVerificationCode]:
    try:
        return EmailVerificationCode.objects.get(email=email)
    except EmailVerificationCode.DoesNotExist:
        return None


def _clean_code_and_user(email: str, existing_code: EmailVerificationCode):
    existing_code.delete()
    try:
        TmpUser.objects.get(email=email).delete()
    except TmpUser.DoesNotExist:
        pass


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
    return timedelta(minutes=10)


class EmailRegistrationException(Exception):
    pass
