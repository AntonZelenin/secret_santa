from datetime import timedelta, datetime, timezone
from typing import Optional

import tools.helpers
from tools.types import Result, Ok, Err
from webapp.models import User, EmailVerificationCode, SetUsernameToken
from webapp import registration, repository


def create_user(email: str):
    if _is_user_already_registered(email):
        # todo what should be the error message?
        raise EmailRegistrationException(
            'This email is already registered. Please use a different email address or sign in'
        )

    existing_user = repository.get_user_by_email(email)
    if existing_user:
        existing_code = _get_existing_code(existing_user)
        if existing_code:
            if existing_code.resend_at < datetime.now(timezone.utc):
                existing_code.delete()
            else:
                # todo what should be the error message?
                raise EmailRegistrationException('Please try in a minute')

    now = datetime.now(timezone.utc)
    if existing_user:
        user = existing_user
    else:
        user = User.objects.create(email=email, username=email, date_joined=now)
    code = tools.helpers.generate_6_digit_code()

    try:
        verification_code = EmailVerificationCode.objects.create(
            user=user,
            code=code,
            created_at=now,
            resend_at=now + timedelta(minutes=1),
            expires_at=now + timedelta(minutes=10),
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
        code_obj = EmailVerificationCode.objects.get(user=User.objects.get(email=email))
        if code_obj.code == code:
            if code_obj.expires_at > datetime.now(timezone.utc):
                return Ok()
            else:
                return Err('The code is expired')
        else:
            return Err('Code has expired')
    except (EmailVerificationCode.DoesNotExist, User.DoesNotExist):
        return Err('Invalid code')


def delete_email_verification_code(email: str):
    try:
        EmailVerificationCode.objects.get(user=User.objects.get(email=email)).delete()
    except (EmailVerificationCode.DoesNotExist, User.DoesNotExist):
        pass


def mark_email_as_verified(email: str):
    user = User.objects.get(email=email)
    user.email_verified = True
    user.save()


def set_password(email: str, password: str):
    user = User.objects.get(email=email)
    user.password = password
    user.save()


def create_set_username_token(email: str) -> SetUsernameToken:
    user = User.objects.get(email=email)
    now = datetime.now(timezone.utc)

    set_username_token = SetUsernameToken(
        user=user,
        token=tools.helpers.generate_random_string(),
        created_at=now,
        expires_at=now + timedelta(minutes=10),
    )
    set_username_token.save()

    return set_username_token


def _get_existing_code(user: User) -> Optional[EmailVerificationCode]:
    try:
        return EmailVerificationCode.objects.get(user=user)
    except EmailVerificationCode.DoesNotExist:
        return None


def _is_user_already_registered(email: str) -> bool:
    try:
        user = User.objects.get(email=email)
        return user.finished_registration
    except User.DoesNotExist:
        return False


class EmailRegistrationException(Exception):
    pass
