from django.core.management import call_command
from django.core.management.base import BaseCommand
import time
class Command(BaseCommand):

    def handle(self, *args, **options):
        maximumTries = 5
        tries = 0
        migrateSuccess = False;
        try:
            while tries < maximumTries and not migrateSuccess:
                try:
                    call_command('migrate')
                    migrateSuccess = True
                except:
                    print("Failed -> trying again")
                    print("waiting 5 seconds")
                    tries += 1
                    time.sleep(5)

            initSuperuserSuccess = False
            if(migrateSuccess):
                tries = 0
                while tries < maximumTries and not initSuperuserSuccess:
                    try:
                        call_command('init_superuser')
                        initSuperuserSuccess = True
                    except:
                        print("Super User Failed -> trying again")
                        tries += 1
                        time.sleep(5)
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('Interrupted - Stopping'))

        self.stdout.write(self.style.SUCCESS("Setup successful"))

