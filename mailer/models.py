from django.db import models

NULLABLE = {'blank': True, 'null': True}
class Boat(models.Model):
    name = models.CharField(max_length=50, verbose_name='название')
    year = models.PositiveSmallIntegerField(**NULLABLE, verbose_name='год выпуска')


