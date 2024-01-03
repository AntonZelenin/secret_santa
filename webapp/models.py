from django.db import models


# Create your models here.
class TmpUser(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, null=True)
    # google_id = models.CharField(max_length=128, null=True)
    # google_token = models.CharField(max_length=128, null=True)
    # google_refresh_token = models.CharField(max_length=128, null=True)
    # google_token_expiration = models.DateTimeField(null=True)
    # email_verification_code = models.CharField(max_length=128, null=True)
    # email_verification_code_expiration = models.DateTimeField(null=True)
    email_verified = models.BooleanField(default=False)
    # password_reset_code = models.CharField(max_length=128, null=True)
    # password_reset_code_expiration = models.DateTimeField(null=True)
    # password_reset = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)


class EmailVerificationCode(models.Model):
    code = models.CharField(max_length=6, unique=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True)
