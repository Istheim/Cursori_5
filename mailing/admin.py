from django.contrib import admin

# Register your models here.
from django.contrib import admin

from mailing.models import Message, Sending, Log

admin.site.register(Message)


@admin.register(Sending)
class SendingAdmin(admin.ModelAdmin):

    list_display = ('user', 'get_customer', 'message', 'created_at',
                    'frequency', 'status_sending', 'start_sending_date', 'start_sending_time')
    readonly_fields = ('created_at',)


@admin.register(Log)
class SendingAdmin(admin.ModelAdmin):
    list_display = ('sending', 'last_attempt', 'status_attempt', 'answer_server')
    readonly_fields = ('sending', 'last_attempt', 'status_attempt', 'answer_server')