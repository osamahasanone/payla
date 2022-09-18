import pytest
from django.conf import settings
from django.core import mail
from model_bakery import baker

from core.models import User
from newsletter.models import SubscriptionAttempt, UnsubscriptionAttempt

pytestmark = pytest.mark.django_db


def test_creating_user_creats_client():
    user = baker.make(User)
    assert user.client is not None


def test_assert_creating_subscription_attempt_sends_email(unsubscribed_client):
    attempt = baker.make(SubscriptionAttempt, client=unsubscribed_client)
    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == settings.SUBSCRIPTION_CONFIRMATION_EMAIL_SUBJECT
    assert mail.outbox[0].to == [unsubscribed_client.user.email]
    assert str(unsubscribed_client) in mail.outbox[0].body
    attempt = SubscriptionAttempt.objects.first()
    assert attempt.confirmation_url in mail.outbox[0].body


def test_assert_creating_unsubscription_attempt_sends_email(subscribed_client):
    attempt = baker.make(UnsubscriptionAttempt, client=subscribed_client)
    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == settings.UNSUBSCRIPTION_CONFIRMATION_EMAIL_SUBJECT
    assert mail.outbox[0].to == [subscribed_client.user.email]
    assert str(subscribed_client) in mail.outbox[0].body
    attempt = UnsubscriptionAttempt.objects.first()
    assert attempt.confirmation_url in mail.outbox[0].body
