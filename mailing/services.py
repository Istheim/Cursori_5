from datetime import timedelta

from mailing.models import Sending


def install_next_date(sending: Sending):
    if sending.frequency == sending.DAILY:
        sending.start_sending_date += timedelta(days=1)
    elif sending.frequency == sending.WEEKLY:
        sending.start_sending_date += timedelta(days=7)
    else:
        sending.start_sending_date += timedelta(days=30)

    return sending.start_sending_date
