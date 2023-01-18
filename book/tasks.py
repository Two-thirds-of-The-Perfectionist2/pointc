from django.core.mail import send_mail
from celery import shared_task
from decouple import config


@shared_task
def send_activation_code(email, activation_code):
    activation_link = f'http://{config("CURRENT_HOST")}/users/activate/{activation_code}/'
    message = f"""
               Hello! Thank you for joined our family. \n  

               Activate your account with a link: \n {activation_link}
               """
    send_mail("Activate account", message, 'admin@admin.com', recipient_list=[email])


@shared_task
def send_code_for_reset(email, activation_code):
    message = f'Nobody dont know this code!\nReset your password with this code:\n{activation_code}'
    send_mail("Drop password", message, 'admin@admin.com', recipient_list=[email], fail_silently=False)
