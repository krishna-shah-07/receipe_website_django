from vege.models import recipe
from django.core.mail import send_mail
from django.conf import settings

def send_email_to_client(request):
    subject = 'Thank you for your order'
    message = 'We hope you enjoy your order'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['emailname@gmail.com']

    send_mail(subject, message, email_from, recipient_list)