from django.contrib import admin
from .models import Client, Newsletter, NewsletterMessage
from django.utils import timezone
from datetime import timedelta
from email.message import EmailMessage
import smtplib
import logging
from logging.handlers import SMTPHandler
import os

def send_newsletter(newsletter):
    subject = f'Newsletter - {timezone.now().date().strftime("%d/%m/%Y")}'
    body = f"""
    <h3>Newsletter for {timezone.now().date().strftime('%d/%m/%y')}</h3>
    <p>Hello,</p>
    <p>{newsletter.message}</p>
    """

    if newsletter.is_error:
        logging.error(f'Error sending newsletter to {len(newsletter.clients)} clients!')
    else:
        success = []
        error = []

        for client in newsletter.clients.all():
            try:
