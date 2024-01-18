from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    email_verified = models.BooleanField(default=False)
    finished_registration = models.BooleanField(default=False)
    # google_id = models.CharField(max_length=128, null=True)
    # google_token = models.CharField(max_length=128, null=True)
    # google_refresh_token = models.CharField(max_length=128, null=True)
    # google_token_expiration = models.DateTimeField(null=True)
    # email_verification_code = models.CharField(max_length=128, null=True)
    # email_verification_code_expiration = models.DateTimeField(null=True)
    # password_reset_code = models.CharField(max_length=128, null=True)
    # password_reset_code_expiration = models.DateTimeField(null=True)
    # password_reset = models.BooleanField(default=False)
    # updated_at = models.DateTimeField(auto_now=True)


# todo delete used codes
class EmailVerificationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField()
    resend_at = models.DateTimeField()
    expires_at = models.DateTimeField()


class SetUsernameToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField()
    expires_at = models.DateTimeField()
