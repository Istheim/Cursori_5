from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@gmail.com',
            is_staff=True,
            is_active=True,
            is_superuser=True,
            verify_code='1234'
        )
        user.set_password('asdfgt173')
        user.save()