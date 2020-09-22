from django.shortcuts import render, redirect
import logging
from django.views import View
from django.contrib import messages
from testcelery.tasks import send_review_email_task

# Create your views here.

logger = logging.getLogger("error")


class ContactView(View):
    def get(self, request):
        messages.info(request, "Fill in the following form.")
        return render(request, "nichiei/contact.html")

    def post(self, request):
        logger.error("print contact email")
        name = request.POST["name"]
        email = request.POST["email"]
        subject = request.POST["subject"]
        message = request.POST["message"]
        send_review_email_task.delay("contact_email_message.txt", name, email, '[contact message]' + subject, message)
        messages.success(request, "We will contact with you ASAP.")

        return render(request, "nichiei/contact.html")
