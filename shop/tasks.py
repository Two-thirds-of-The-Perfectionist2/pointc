from django.core.mail import send_mail
from celery import shared_task
from decouple import config


@shared_task
def send_confirmation_code(email, activation_code):
    activation_link = f'http://{config("CURRENT_HOST")}/deliveries/accept/{activation_code}/'
    message = f"""
               Hello! Thank you for using our service. \n  

               Pleaze confirm your order with a link: \n {activation_link}
               """
    send_mail("Confirm your order", message, 'admin@admin.com', recipient_list=[email])
