import arrow
import pytest
from django.conf import settings
from django.core import mail
from django.test import override_settings
from freezegun.api import freeze_time
from model_bakery import baker

from newsletter.errors import AlreadySubscriber, SubscriptionConfirmationFailed
from newsletter.models import SubscriptionAttempt
from newsletter.services.subscription import confirm as confirm_subscription
from newsletter.services.subscription import start as start_subscription

pytestmark = pytest.mark.django_db

# Tests for start subscription


def test_start_subscription_success_creates_attempt(unsubscribed_client):
    start_subscription(unsubscribed_client)
    assert SubscriptionAttempt.objects.count() == 1


def test_start_subscription_success_sends_email_to_client(unsubscribed_client):
    start_subscription(unsubscribed_client)
    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == settings.SUBSCRIPTION_CONFIRMATION_EMAIL_SUBJECT
    assert mail.outbox[0].to == [unsubscribed_client.user.email]
    assert str(unsubscribed_client) in mail.outbox[0].body
    attempt = SubscriptionAttempt.objects.first()
    assert attempt.confirmation_url in mail.outbox[0].body


def test_start_subscription_keeps_client_unsubscribed(unsubscribed_client):
    start_subscription(unsubscribed_client)
    unsubscribed_client.refresh_from_db()
    assert not unsubscribed_client.subscribed


def test_start_subscription_fails_when_client_already_subscribed(subscribed_client):
    with pytest.raises(AlreadySubscriber):
        start_subscription(subscribed_client)


# Tests for confirm subscription


def test_confirm_subscription_success(unsubscribed_client):
    sub_attempt = baker.make(
        SubscriptionAttempt,
        client=unsubscribed_client,
        valid_from=arrow.utcnow().shift(hours=-2).datetime,
        valid_to=arrow.utcnow().shift(hours=+2).datetime,
        confirmed_at=None,
    )

    confirm_subscription(sub_attempt.secret_code)

    sub_attempt.refresh_from_db()
    assert sub_attempt.confirmed_at is not None
    unsubscribed_client.refresh_from_db()
    assert unsubscribed_client.subscribed


def test_confirm_subscription_fails_when_attempt_not_found():
    with pytest.raises(SubscriptionConfirmationFailed):
        confirm_subscription("unkonwn_secret_code")


def test_confirm_subscription_fails_when_client_already_subscribed(subscribed_client):
    sub_attempt = baker.make(
        SubscriptionAttempt,
        client=subscribed_client,
        valid_from=arrow.utcnow().shift(days=-1).datetime,
        valid_to=arrow.utcnow().shift(days=+1).datetime,
        confirmed_at=None,
    )
    with pytest.raises(SubscriptionConfirmationFailed):
        confirm_subscription(sub_attempt.secret_code)


# user received a confirmation email, confirmed it, then tried to confirm again
def test_confirm_subscription_fails_when_attempt_already_confirmed(unsubscribed_client):
    sub_attempt = baker.make(
        SubscriptionAttempt,
        client=unsubscribed_client,
        valid_from=arrow.utcnow().shift(days=-1).datetime,
        valid_to=arrow.utcnow().shift(days=+1).datetime,
        confirmed_at=arrow.utcnow().datetime,
    )
    with pytest.raises(SubscriptionConfirmationFailed):
        confirm_subscription(sub_attempt.secret_code)


@override_settings(CONFIRMATION_LINK_VALIDITY_HOURS=1)
@freeze_time("2022-09-01 12:00:00", tz_offset=0)
def test_confirm_subscription_fails_when_attempt_is_expired(unsubscribed_client):
    sub_attempt = baker.make(
        SubscriptionAttempt,
        client=unsubscribed_client,
        valid_from=arrow.utcnow().shift(hours=-24).datetime,
        confirmed_at=None,
    )

    with pytest.raises(SubscriptionConfirmationFailed):
        confirm_subscription(sub_attempt.secret_code)
