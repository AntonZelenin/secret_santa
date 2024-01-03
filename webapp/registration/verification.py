from webapp.registration import sender


def send_verification_code(email: str, code: str):
    sender.send_email()
    # raise VerificationEmailSendingException('failed to send verification registration')


class VerificationEmailSendingException(Exception):
    pass
