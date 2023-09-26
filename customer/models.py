from django.db import models

# Create your models here.
from django.db import models

from users.models import User, NULLABLE


class Customer(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создатель', **NULLABLE)
    first_name = models.CharField(max_length=20, verbose_name='Имя')
    last_name = models.CharField(max_length=20, verbose_name='Фамилия')
    email = models.EmailField(unique=True, verbose_name='Почта клиента')
    comment = models.TextField(verbose_name='Комментарий')

    def __str__(self):
        return f'{self.first_name} || {self.last_name}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    permissions = {
        ('can_view_customers', 'Can view customers')
    }
