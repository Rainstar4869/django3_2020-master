from django.shortcuts import render
from .tasks import send_review_email_task


# Create your views here.


def test_celery_mail(name, email, review):
    send_review_email_task(name, email, review)
