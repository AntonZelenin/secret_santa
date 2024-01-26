from django.template.loader import render_to_string

from tools import email_sender, helpers


def send_verification_code(email: str):
    code = helpers.generate_6_digit_code()
    try:
        email_sender.send(
            email,
            'Email verification',
            code,
        )
    except Exception as e:
        raise VerificationEmailSendingException(f'Failed to send verification email: {e}')

    return code


def _get_verification_email_template(code: str) -> str:
    return render_to_string('email/verification.html', {'code': code})


class VerificationEmailSendingException(Exception):
    pass
