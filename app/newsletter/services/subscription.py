from django.db import transaction
from django.utils import timezone

from newsletter.errors import AlreadySubscriber, SubscriptionConfirmationFailed
from newsletter.models import Client, SubscriptionAttempt
from newsletter.services.transaction import get_secret


def start(client: Client) -> SubscriptionAttempt:
    if client.subscribed:
        raise AlreadySubscriber
    return SubscriptionAttempt.objects.create(
        client=client, secret_code=get_secret(SubscriptionAttempt)
    )


@transaction.atomic
def confirm(secret_code: str) -> bool:
    now = timezone.now()
    attempt = (
        SubscriptionAttempt.objects.select_related("client")
        .filter(
            secret_code=secret_code,
            confirmed_at__isnull=True,
            valid_from__lte=now,
            valid_to__gte=now,
            client__subscribed=False,
        )
        .first()
    )

    if not attempt:
        raise SubscriptionConfirmationFailed

    attempt.confirmed_at = now
    attempt.save()
    attempt.client.subscribed = True
    attempt.client.save()
