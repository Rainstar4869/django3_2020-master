from django.template import Context
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings


def send_review_email(template, name, email, subject, review):
    context = {
        'name': name,
        'email': email,
        'review': review,
    }

    email_subject = subject
    email_body = render_to_string(template, context)

    email = EmailMessage(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL, [settings.NICHIEI_INFO["CONTACT_INFO_EMAIL"]],
    )
    return email.send(fail_silently=False)
