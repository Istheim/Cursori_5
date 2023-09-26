from builtins import *
from datetime import datetime, date, time

from django.core.mail import send_mail

from mailing.models import Sending, Log
from mailing.services import install_next_date
from config import settings


def sending_mail():
    query_sending = Sending.objects.exclude(status_sending=Sending.COMPLETED) \
        .filter(start_sending_date=date.today()) \
        .filter(start_sending_time__lte=time(*list(map(int, datetime.now().time().strftime("%H:%M:%S").split(':')))))

    for sending in query_sending:
        email_list = [x.email for x in sending.customer.all()]
        sending.status_sending = Sending.ACTIVATED
        sending.save()
        try:
            result = send_mail(
                subject=sending.message.subject,
                message=sending.message.content,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=email_list,
                fail_silently=False
            )
            if result:
                Log.objects.create(sending=sending,
                                   last_attempt=datetime.now(),
                                   status_attempt='success',
                                   answer_server='200')
                sending.start_sending_date = install_next_date(sending)
                sending.save()
        except Exception as error:
            Log.objects.create(sending=sending,
                               last_attempt=datetime.now(),
                               status_attempt='failure',
                               answer_server=error)