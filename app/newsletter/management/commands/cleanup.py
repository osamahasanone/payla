from django.core.management.base import BaseCommand

from newsletter.models import SubscriptionAttempt, UnsubscriptionAttempt


class Command(BaseCommand):
    help = "Remove outdated temporary records from the database"

    def handle(self, *args, **kwargs):
        SubscriptionAttempt.objects.outdated().delete()
        UnsubscriptionAttempt.objects.outdated().delete()
        self.stdout.write("subscription and unubscription attempts have been cleaned!")
