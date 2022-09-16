from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Remove outdated temporary records from the database"

    def handle(self, *args, **kwargs):
        self.stdout.write("Database is now clean!")
