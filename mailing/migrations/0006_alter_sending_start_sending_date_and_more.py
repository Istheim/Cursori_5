# Generated by Django 4.2.5 on 2023-09-26 16:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0005_alter_sending_start_sending_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sending',
            name='start_sending_date',
            field=models.DateField(default=datetime.datetime(2023, 9, 26, 16, 4, 24, 990046, tzinfo=datetime.timezone.utc), verbose_name='Дата начала'),
        ),
        migrations.AlterField(
            model_name='sending',
            name='start_sending_time',
            field=models.TimeField(blank=True, default=datetime.time(19, 4, 24, 990175), null=True, verbose_name='время рассылки'),
        ),
    ]