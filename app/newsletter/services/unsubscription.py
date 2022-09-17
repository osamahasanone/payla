from django.db import transaction
from django.utils import timezone

from newsletter.errors import AlreadyUnsubscriber, UnsubscriptionConfirmationFailed
from newsletter.models import Client, UnsubscriptionAttempt
from newsletter.services.secret_generator import get_secret


def start(client: Client) -> None:
    if not client.subscribed:
        raise AlreadyUnsubscriber
    UnsubscriptionAttempt.objects.create(
        client=client, secret_code=get_secret(UnsubscriptionAttempt)
    )


@transaction.atomic
def confirm(secret_code: str) -> bool:
    now = timezone.now()
    attempt = (
        UnsubscriptionAttempt.objects.select_related("client")
        .filter(
            secret_code=secret_code,
            confirmed_at__isnull=True,
            valid_from__lte=now,
            valid_to__gte=now,
            client__subscribed=True,
        )
        .first()
    )

    if not attempt:
        raise UnsubscriptionConfirmationFailed

    attempt.confirmed_at = now
    attempt.save()
    attempt.client.subscribed = False
    attempt.client.save()
