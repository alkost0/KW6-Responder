
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_letter', models.CharField(max_length=100, verbose_name='Тема рассылки')),
                ('body_letter', models.TextField(verbose_name='Тело рассылки')),
            ],
            options={
                'verbose_name': 'сообщение',
                'verbose_name_plural': 'сообщения',
            },
        ),
        migrations.CreateModel(
            name='Mailer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_start', models.DateTimeField(verbose_name='Дата и время начала рассылки')),
                ('date_end', models.DateTimeField(verbose_name='Дата и время окончания рассылки')),
                ('periodicity', models.CharField(choices=[('DAILY', 'ежедневно'), ('WEEKLY', 'еженедельно'), ('MONTHLY', 'ежемесячно')], max_length=50, verbose_name='Периодичность')),
                ('status', models.CharField(choices=[('created', 'создана'), ('started', 'запущена'), ('closed', 'завершена')], default='created', max_length=50, verbose_name='Статус')),
                ('client', models.ManyToManyField(to='client.client', verbose_name='Кому')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailer.message', verbose_name='Сообщение')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'рассылка',
                'verbose_name_plural': 'рассылки',
            },
        ),
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_try', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время последней попытки отправки')),
                ('status_try', models.CharField(max_length=50, verbose_name='Статус попытки')),
                ('answer', models.CharField(max_length=250, null=True, verbose_name='Ответ сервера')),
                ('mailer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailer.mailer', verbose_name='Рассылка')),
            ],
            options={
                'verbose_name': 'лог',
                'verbose_name_plural': 'логи',
            },
        ),
    ]
