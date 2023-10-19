
from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('body', models.TextField(verbose_name='Содержание')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='blog/', verbose_name='Изображение')),
                ('view_count', models.IntegerField(default=0, verbose_name='Количество просмотров')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
            ],
            options={
                'verbose_name': 'статья',
                'verbose_name_plural': 'статьи',
            },
        ),
    ]
