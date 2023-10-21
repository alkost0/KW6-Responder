from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.utils import timezone

from client.models import Client
from mailer.models import Mailer


def send_message_email(mailer_item: Mailer):
    now = timezone.localtime(timezone.now())

    recepients = [client.email for client in mailer_item.client.all()]
    if mailer_item.date_start <= now <= mailer_item.date_end:
        send_mail(
         f"{mailer_item.message.subject_letter}",
         f"{mailer_item.message.body_letter}",
         settings.EMAIL_HOST_USER,
         recepients
        )
        mailer_item.status = 'started'
        mailer_item.save()


def get_cache_count_mailer():
    if settings.CACHE_ENABLED:
        key = 'mailer'
        mailer = cache.get(key)
        if mailer is None:
            mailer = Mailer.objects.all().count()
            cache.set(key, mailer)
    else:
        mailer = Mailer.objects.all().count()
    return mailer


def get_cache_count_client():
    if settings.CACHE_ENABLED:
        key = 'client'
        client = cache.get(key)
        if client is None:
            client = Client.objects.all().count()
            cache.set(key, client)
    else:
        client = Client.objects.all().count()
    return client
