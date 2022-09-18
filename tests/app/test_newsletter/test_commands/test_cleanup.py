import arrow
import pytest
from django.core.management import call_command
from django.test import override_settings
from freezegun.api import freeze_time
from model_bakery import baker

from core.models import User
from newsletter.models import Client, SubscriptionAttempt, UnsubscriptionAttempt

pytestmark = pytest.mark.django_db


@override_settings(CONFIRMATION_LINK_VALIDITY_HOURS=1)
@freeze_time("2022-09-01 12:00:00", tz_offset=0)
def test_cleanup():
    # 2 clients
    baker.make(User, _quantity=2)

    for client in Client.objects.all():
        for model in [SubscriptionAttempt, UnsubscriptionAttempt]:
            # outdated (should be cleaned)
            baker.make(
                model,
                client=client,
                valid_from=arrow.utcnow().shift(hours=-24).datetime,
                confirmed_at=None,
            )
            # confirmed - should not be cleaned
            baker.make(
                model,
                client=client,
                confirmed_at=arrow.utcnow().datetime,
            )
            # not confirmed but still valid - should not be cleaned
            baker.make(
                model,
                client=client,
                confirmed_at=arrow.utcnow().datetime,
            )

    call_command("cleanup")

    assert SubscriptionAttempt.objects.filter().count() == 4
    assert UnsubscriptionAttempt.objects.filter().count() == 4
