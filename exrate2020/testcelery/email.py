from django.template import Context
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMultiAlternatives


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


def send_multialternatives_mail(mailtype, subject, context, to_email, txt_template=None, html_template=None):
    if mailtype == "both":
        send_bothtype_mail(subject, context, to_email, txt_template, html_template)
    else:
        send_txt_mail(subject, context, to_email, txt_template)


def send_txt_mail(subject, context, to_email, txt_template):
    email_subject = subject
    email_body = render_to_string(txt_template, context)

    email = EmailMessage(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL, [to_email],
    )
    return email.send(fail_silently=False)

def send_bothtype_mail(subject, context, to_email, txt_template, html_template):
    subject, from_email = subject, settings.DEFAULT_FROM_EMAIL
    text_content = render_to_string(txt_template, context)
    html_content = render_to_string(html_template, context)

    email = EmailMultiAlternatives(
        subject,
        text_content,
        from_email,
        [to_email])
    email.attach_alternative(html_content, "text/html")
    return email.send(fail_silently=False)
