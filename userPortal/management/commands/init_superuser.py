from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Initialize superuser'

    #NOTE: MUST GET DEFAULT FROM SECRET KEYS!!!
    def handle(self, *args, **options):
        User = get_user_model()

        if not User.objects.filter(username='sample1').exists():
            User.objects.create_superuser(
                username='sample1',
                email='sample1@gmail.com',
                password='123'
            )

        self.stdout.write(self.style.SUCCESS('Defualt User created'))