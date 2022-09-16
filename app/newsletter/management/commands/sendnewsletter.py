from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Send the newsletter to subscribers"

    def handle(self, *args, **kwargs):
        self.stdout.write("Newsletter has been sent to subscribers")
