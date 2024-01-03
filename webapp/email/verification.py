from webapp.email import sender


def send_verification_code(email: str, code: str):
    sender.send_email()
    # raise VerificationEmailSendingException('failed to send verification email')


class VerificationEmailSendingException(Exception):
    pass
