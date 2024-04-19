from config.celery import app
from .utils import send_activation_code
from django.core.mail import send_mail


@app.task
def send_activation_code_celery(email, activation_code):
    send_activation_code(email, activation_code)