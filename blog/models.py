from django.db import models

# Create your models here.
from django.db import models

from users.models import NULLABLE


class Blog(models.Model):
    title = models.CharField(max_length=30, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    image = models.ImageField(upload_to='blog', verbose_name='Изображение', **NULLABLE)
    count_views = models.IntegerField(default=0, verbose_name='Количество просмотров')
    date_published = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'