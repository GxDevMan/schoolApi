from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import connections
import time


class Command(BaseCommand):
    """Django command to pause execution until database is available"""

    def handle(self, *args, **options):
        maximumTries = 5
        tries = 0
        self.stdout.write("Waiting for database...")
        db_conn = None

        while db_conn is None and tries < maximumTries:
            try:
                db_conn = connections["default"]
                User = get_user_model()
                User.objects.filter(username='sample1')

                print("success")
                print("Db_conn: " + str(db_conn is None))
                print("tries < maximumTries " + str(tries < maximumTries))
                print("")
            except:
                print("Failed")
                self.stdout.write("Database unavailable, waiting 5 second...")
                tries += 0
                time.sleep(5)

        self.stdout.write(self.style.SUCCESS("Database available!"))