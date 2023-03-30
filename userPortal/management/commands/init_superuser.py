import os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Initialize superuser'

    #NOTE: MUST GET DEFAULT FROM SECRET KEYS!!!
    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get('DEFAULT_USER')
        email = os.environ.get('DEFAULT_EMAIL')
        password = username

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )

        self.stdout.write(self.style.SUCCESS('Defualt User created'))