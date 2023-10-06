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

msg = EmailMessage()
msg[‘Subject’] = subject
msg.set_content(body)
msg[‘From’] = ‘noreply@example.com’
msg[‘To’] = client.email
smtp = smtplib.SMTP(‘localhost’)
smtp.send_message(msg)
success.append(client)
except Exception as e:
error.append({‘client’: client, ‘error’: str(e)})

    newsletter.log.create(
        last_attempted=timezone.now(),
        status='error' if error else 'success',
        errors=error if error else None
    )
class NewsletterAdmin(admin.ModelAdmin):
list_display = [‘id’, ‘name’, ‘periodicity’, ‘status’]
list_filter = [‘status’]
search_fields = [‘name’]

class ClientAdmin(admin.TabularInline):
model = Client
extra = 1

class MessageAdmin(admin.StackedInline):
model = NewsletterMessage
extra = 0

@admin.register(Newsletter)

class NewsletterModelAdmin(NewsletterAdmin):
inlines = [ClientAdmin, MessageAdmin]

admin.site.register(Client)
admin.site.register(Newsletter, NewsletterModelAdmin)
admin.site.unregister(NewsletterMessage)

if name == ‘main’:
os.environ.setdefault(‘DJANGO_SETTINGS_MODULE’, ‘your_app_name.settings’)
from django.core.management import execute_from_command_line
execute_from_command_line(sys.argv)
