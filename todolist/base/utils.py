from django.conf import settings
from django.core.mail import send_mail


def send_email_token(email,token):
    try:
        subject = 'Otp for email verification'
        message = f'Your otp for email verification is {token}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail( subject, message, email_from, recipient_list )

    except Exception as e:
        return False

    return True