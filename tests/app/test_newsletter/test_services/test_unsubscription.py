import arrow
import pytest
from django.conf import settings
from django.core import mail
from django.test import override_settings
from freezegun.api import freeze_time
from model_bakery import baker

from newsletter.errors import AlreadyUnsubscriber, UnsubscriptionConfirmationFailed
from newsletter.models import UnsubscriptionAttempt
from newsletter.services.unsubscription import confirm as confirm_unsubscription
from newsletter.services.unsubscription import start as start_unsubscription

pytestmark = pytest.mark.django_db

# Tests for start unsubscription


def test_start_unsubscription_success_creates_attempt(subscribed_client):
    start_unsubscription(subscribed_client)
    assert UnsubscriptionAttempt.objects.count() == 1


def test_start_unsubscription_success_sends_email_to_client(subscribed_client):
    start_unsubscription(subscribed_client)
    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == settings.UNSUBSCRIPTION_CONFIRMATION_EMAIL_SUBJECT
    assert mail.outbox[0].to == [subscribed_client.user.email]
    assert str(subscribed_client) in mail.outbox[0].body
    attempt = UnsubscriptionAttempt.objects.first()
    assert attempt.confirmation_url in mail.outbox[0].body


def test_start_unsubscription_keeps_client_subscribed(subscribed_client):
    start_unsubscription(subscribed_client)
    subscribed_client.refresh_from_db()
    assert subscribed_client.subscribed


def test_start_unsubscription_fails_when_client_already_unsubscribed(
    unsubscribed_client,
):
    with pytest.raises(AlreadyUnsubscriber):
        start_unsubscription(unsubscribed_client)


# Tests for confirm unsubscription


def test_confirm_unsubscription_success(subscribed_client):
    attempt = baker.make(
        UnsubscriptionAttempt,
        client=subscribed_client,
        valid_from=arrow.utcnow().shift(hours=-2).datetime,
        valid_to=arrow.utcnow().shift(hours=+2).datetime,
        confirmed_at=None,
    )

    confirm_unsubscription(attempt.secret_code)

    attempt.refresh_from_db()
    assert attempt.confirmed_at is not None
    subscribed_client.refresh_from_db()
    assert not subscribed_client.subscribed


def test_confirm_unsubscription_fails_when_attempt_not_found():
    with pytest.raises(UnsubscriptionConfirmationFailed):
        confirm_unsubscription("unkonwn_secret_code")


def test_confirm_unsubscription_fails_when_client_already_unsubscribed(
    unsubscribed_client,
):
    attempt = baker.make(
        UnsubscriptionAttempt,
        client=unsubscribed_client,
        valid_from=arrow.utcnow().shift(days=-1).datetime,
        valid_to=arrow.utcnow().shift(days=+1).datetime,
        confirmed_at=None,
    )
    with pytest.raises(UnsubscriptionConfirmationFailed):
        confirm_unsubscription(attempt.secret_code)


# user received a confirmation email, confirmed it, then tried to confirm again
def test_confirm_unsubscription_fails_when_attempt_already_confirmed(
    unsubscribed_client,
):
    attempt = baker.make(
        UnsubscriptionAttempt,
        client=unsubscribed_client,
        valid_from=arrow.utcnow().shift(days=-1).datetime,
        valid_to=arrow.utcnow().shift(days=+1).datetime,
        confirmed_at=arrow.utcnow().datetime,
    )
    with pytest.raises(UnsubscriptionConfirmationFailed):
        confirm_unsubscription(attempt.secret_code)


@override_settings(CONFIRMATION_LINK_VALIDITY_HOURS=1)
@freeze_time("2022-09-01 12:00:00", tz_offset=0)
def test_confirm_unsubscription_fails_when_attempt_is_expired(unsubscribed_client):
    sub_attempt = baker.make(
        UnsubscriptionAttempt,
        client=unsubscribed_client,
        valid_from=arrow.utcnow().shift(hours=-24).datetime,
        confirmed_at=None,
    )

    with pytest.raises(UnsubscriptionConfirmationFailed):
        confirm_unsubscription(sub_attempt.secret_code)
