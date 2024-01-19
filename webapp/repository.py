from typing import Optional

from webapp.models import User, EmailVerificationCode


def get_user(user_id: int) -> Optional[User]:
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None


def get_user_by_email(email: str) -> Optional[User]:
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None

def get_email_verification_code(user: User) -> Optional[EmailVerificationCode]:
    try:
        return EmailVerificationCode.objects.get(user=user)
    except EmailVerificationCode.DoesNotExist:
        return None
