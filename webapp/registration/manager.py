import logging
from contextlib import suppress
from datetime import timedelta, datetime, timezone
from typing import Optional

import tools.helpers
from tools.types import Result, Ok, Err
from webapp.models import User, EmailVerificationCode, SetUsernameToken
from webapp import registration, repository

logger_ = logging.getLogger(__name__)


def create_user(email: str) -> User:
    if _is_user_already_registered(email):
        raise EmailRegistrationException(
            'This email is already registered. Please use a different email address or sign in'
        )

    if user := repository.get_user_by_email(email):
        resend_verification_code(user.id)
        return user

    user = User.objects.create(email=email, username=email, date_joined=datetime.now(timezone.utc))
    try:
        send_verification_code(user)
    except Exception:
        user.delete()
        raise

    return user


def resend_verification_code(user_id: int) -> User:
    user = User.objects.get(id=user_id)

    if _is_user_already_registered(user.email):
        raise EmailRegistrationException(
            'This email is already registered. Please use a different email address or sign in'
        )

    if not _can_send_verification_code(user.email):
        raise VerificationCodeException('Please try in a minute')

    _cleanup_existing_code(user.email)

    send_verification_code(user)

    return user


def send_verification_code(user: User):
    now = datetime.now(timezone.utc)
    code = tools.helpers.generate_6_digit_code()

    try:
        verification_code = EmailVerificationCode.objects.create(
            user=user,
            code=code,
            created_at=now,
            # todo change to 1 minute
            resend_at=now + timedelta(seconds=10),
            expires_at=now + timedelta(minutes=10),
        )
    except Exception as e:
        logger_.error(e)

        # todo users should no get such a message
        raise Exception('Failed to create the verification code')

    try:
        registration.verification.send_verification_code(user.email, 'some random code')
    except Exception as e:
        verification_code.delete()
        raise VerificationCodeException(e)


def _can_send_verification_code(email: str) -> bool:
    """
    Verification code can be sent either if it's a new user that doesn't exist yet
    or if resend cooldown has passed
    """

    if user := repository.get_user_by_email(email):
        existing_code = repository.get_email_verification_code(user)
        return existing_code and existing_code.resend_at < datetime.now(timezone.utc)

    return True


def _cleanup_existing_code(email: str):
    if user := repository.get_user_by_email(email):
        if verification_code := repository.get_email_verification_code(user):
            verification_code.delete()


def check_code(user_id: int, code: str) -> Result[bool]:
    # todo prevent brute force attacks
    try:
        user = User.objects.get(id=user_id)
        code_obj = EmailVerificationCode.objects.get(user=user)
        # todo bring back this check
        # todo first check if code is expired
        # if code_obj.code == code:
        if '000000' == code:
            if code_obj.expires_at > datetime.now(timezone.utc):
                return Ok()
            else:
                return Err('The code is expired')
        else:
            return Err('Invalid code')
    except (EmailVerificationCode.DoesNotExist, User.DoesNotExist):
        return Err('Invalid code')


def delete_email_verification_code(user_id: int):
    with suppress(EmailVerificationCode.DoesNotExist, User.DoesNotExist):
        EmailVerificationCode.objects.get(user=User.objects.get(id=user_id)).delete()


def mark_email_as_verified(user_id: int):
    user = User.objects.get(id=user_id)
    user.email_verified = True
    user.save()


def set_password(user_id: int, password: str):
    user = User.objects.get(id=user_id)
    user.set_password(password)
    user.save()


def create_set_username_token(user_id: int) -> SetUsernameToken:
    user = User.objects.get(id=user_id)
    now = datetime.now(timezone.utc)

    set_username_token = SetUsernameToken(
        user=user,
        token=tools.helpers.generate_random_string(),
        created_at=now,
        expires_at=now + timedelta(minutes=10),
    )
    set_username_token.save()

    return set_username_token


def _is_user_already_registered(email: str) -> bool:
    try:
        user = User.objects.get(email=email)
        return user.finished_registration
    except User.DoesNotExist:
        return False


def get_next_step(current_step: str) -> Optional[str]:
    if current_step == registration.constants.RESEND_VERIFICATION_CODE:
        return registration.constants.VERIFY_EMAIL

    steps = registration.constants.REGISTRATION_STEPS
    curr_step_idx = steps.index(current_step)

    if curr_step_idx == len(steps) - 1:
        return None

    return steps[curr_step_idx + 1]


class EmailRegistrationException(Exception):
    pass


class VerificationCodeException(Exception):
    pass
