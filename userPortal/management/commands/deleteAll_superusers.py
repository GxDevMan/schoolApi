from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'delete all superuser'

    def handle(self, *args, **options):
        try:
            superUsers = User.objects.filter(is_superuser=True)
            superUsers.delete()
            self.stdout.write(self.style.SUCCESS('ALL SUPERUSERS DELETED!!!'))
        except:
            self.stdout.write(self.style.ERROR('Exception Occured'))