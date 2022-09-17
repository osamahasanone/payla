from django.core.management.base import BaseCommand

from newsletter.models import Client
from newsletter.services.email import send_newsletter_email


class Command(BaseCommand):
    help = "Send the newsletter to subscribers"

    def add_arguments(self, parser):
        parser.add_argument(
            "-b", "--batch", type=int, help="How many email should be sent in one go?"
        )

    def handle(self, *args, **kwargs):
        subscribed_clients = Client.objects.subscribed()
        batch_size = kwargs["batch"]
        if batch_size:
            send_newsletter_email(subscribed_clients, batch_size)
        else:
            send_newsletter_email(subscribed_clients)
        self.stdout.write("Newsletter has been sent to subscribers")
