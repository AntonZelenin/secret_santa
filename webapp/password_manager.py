from django.contrib.auth.tokens import default_token_generator

from tools import email_sender, logger
from webapp.models import User

logger = logger.get_logger(__name__)


def generate_password_reset_token(user_id: int) -> str:
    return default_token_generator.make_token(User.objects.get(id=user_id))


def check_password_reset_token(user_id: int, token: str) -> bool:
    return default_token_generator.check_token(User.objects.get(id=user_id), token)


def set_password(user_id: int, password: str):
    user = User.objects.get(id=user_id)
    user.set_password(password)
    user.save()


def request_password_reset(email: str):
    user = User.objects.get(email=email)
    if not user:
        logger.warning(f'Password reset requested for non-existing user with email {email}')
        return

    token = generate_password_reset_token(user.id)
    email_sender.send(
        recipient_email=email,
        subject='Password reset',
        message_text=f'Click here to reset your password: http://localhost:8000/reset-password/{token}'
    )
