from typing import Optional

from webapp.models import User


def get_user_by_email(email: str) -> Optional[User]:
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None
