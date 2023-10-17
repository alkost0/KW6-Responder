from django.db import models
from client.models import Client
from config import settings

NULLABLE = {'blank': True, 'null': True}

PERIODICITY_CHOICES = (
    ('DAILY', 'ежедневно'),
    ('WEEKLY', 'еженедельно'),
    ('MONTHLY', 'ежемесячно')
)

STATUS_CHOICES = (
    ('created', 'создана'),
    ('started', 'запущена'),
    ('closed', 'завершена')
)


class Message(models.Model):
    subject_letter = models.CharField(max_length=100, verbose_name='Тема рассылки')
    body_letter = models.TextField(verbose_name='Содержание рассылки')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE,
                              verbose_name='Пользователь')

    def __str__(self):
        return f'{self.subject_letter}'

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class Mailer(models.Model):
    date_start = models.DateTimeField(verbose_name='Дата и время начала рассылки')
    date_end = models.DateTimeField(verbose_name='Дата и время окончания рассылки')
    periodicity = models.CharField(max_length=50, choices=PERIODICITY_CHOICES, verbose_name='Периодичность')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='created', verbose_name='Статус')

    client = models.ManyToManyField(Client, verbose_name='Кому')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Пользователь')

    def __str__(self):
        return f'{self.date_start}-{self.date_end}:{self.periodicity}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'


class Logs(models.Model):
    last_try = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время последней попытки отправки')
    status_try = models.CharField(max_length=50, verbose_name='Статус попытки')
    answer = models.CharField(max_length=250, null=True, verbose_name='Ответ сервера')

    mailer_id = models.ForeignKey(Mailer, on_delete=models.CASCADE, verbose_name='Рассылка')

    def __str__(self):
        return f'{self.last_try}: {self.status_try}'

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'
