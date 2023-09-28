from builtins import *

from django.db import models

# Create your models here.
from datetime import datetime
from django.utils import timezone

from django.db import models

from customer.models import Customer
from users.models import User


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создатель', default='')
    subject = models.CharField(max_length=50, verbose_name='Тема')
    content = models.TextField(verbose_name='Контент', default='')

    def __str__(self):
        return f'{self.subject}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Sending(models.Model):
    DAILY = 'раз в день'
    WEEKLY = 'раз в неделю'
    MONTHLY = 'раз в месяц'

    INTERVAL = (
        (DAILY, 'раз в день'),
        (WEEKLY, 'раз в неделю'),
        (MONTHLY, 'раз в месяц')
    )
    COMPLETED = 'Завершена'
    CREATED = 'Создана'
    ACTIVATED = 'Запущена'

    STATUS = (
        (COMPLETED, 'завершена'),
        (CREATED, 'создана'),
        (ACTIVATED, 'активирована')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создатель')
    customer = models.ManyToManyField(Customer, verbose_name='Клиент')
    message = models.ForeignKey(Message, on_delete=models.SET_NULL, verbose_name='Сообщение', null=True)
    created_at = models.DateTimeField(editable=True, auto_now=True, verbose_name='Время создания')
    next_run = models.DateTimeField(editable=True, auto_now=True, verbose_name='Дата следующей рассылки')
    frequency = models.CharField(choices=INTERVAL, max_length=30, verbose_name='Периодичность')
    status_sending = models.CharField(choices=STATUS, max_length=30, verbose_name='Статус')
    start_sending_date = models.DateField(default=datetime.now(), verbose_name='Дата начала')
    start_sending_time = models.TimeField(default=datetime.now().time(), verbose_name='время рассылки', blank=True,
                                          null=True)

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

        permissions = [
            (
                'can_view_sending',
                'Can view sending'
            ),
            (
                'can_disable_sending',
                'Can disable sending'
            ),

        ]

    def get_customer(self):
        return ','.join([str(cus) for cus in self.customer.all()])

    def __str__(self):
        return f'{self.id} - {self.message.subject}'


class Log(models.Model):
    STATUS_CHOICES = [
        ('success', 'завершена'),
        ('failure', 'провалена'),
        ('in_progress', 'в процессе'),
    ]

    sending = models.ForeignKey(Sending, on_delete=models.CASCADE, verbose_name='Письмо', blank=True, null=True)
    last_attempt = models.DateTimeField(auto_now_add=True, verbose_name='Дата последней попытки')
    status_attempt = models.CharField(choices=STATUS_CHOICES, max_length=30, default='in_progress',
                                      verbose_name='Текущий статус')
    answer_server = models.CharField(max_length=20, verbose_name='Ответ почтового сервера', default='')

    class Meta:
        verbose_name = 'Журнал'
        verbose_name_plural = 'Журналы'