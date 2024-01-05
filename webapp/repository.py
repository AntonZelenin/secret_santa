from typing import Optional

from webapp.models import TmpUser


def get_tmp_user_by_email(email: str) -> Optional[TmpUser]:
    try:
        return TmpUser.objects.get(email=email)
    except TmpUser.DoesNotExist:
        return None
