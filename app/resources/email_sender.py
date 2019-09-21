from django.core.mail import send_mail

from settings.settings import EMAIL_HOST_USER


def send_forget_email(message, email):
    send_mail("forget password", message, EMAIL_HOST_USER, [email])

def send_signup_email(message, email):
    send_mail("Welcome to Alpha", message, EMAIL_HOST_USER, [email])