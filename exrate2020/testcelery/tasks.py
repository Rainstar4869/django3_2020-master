from celery import shared_task
from celery.decorators import task
from celery.utils.log import get_task_logger

from .email import send_review_email, send_multialternatives_mail

logger = get_task_logger(__name__)


@shared_task
def add(x, y):
    return x + y


@task(name="send_review_email_task")
def send_review_email_task(template, name, email, subject, review):
    logger.info("Sent review email")
    return send_review_email(template, name, email, subject, review)


@task(name="send_multialternatives_mail_task")
def send_multialternatives_mail_task(mailtype, subject, context, toemail, txt_template, html_template):
    return send_multialternatives_mail(mailtype, subject, context, toemail, txt_template, html_template)
