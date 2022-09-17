import pytest
from django.conf import settings
from django.core import mail
from django.urls import reverse
from model_bakery import baker

from core.models import User
from newsletter.services.email import (
    compose_single_newsletter_email,
    newsletter_email_batchs,
    send_newsletter_email,
)

pytestmark = pytest.mark.django_db


def test_compose_single_newsletter_email(subscribed_client):
    email = compose_single_newsletter_email(None, subscribed_client)
    assert email.subject == settings.NEWSLETTER_EMAIL_SUBJECT
    assert email.to == [subscribed_client.user.email]
    assert str(subscribed_client) in email.body
    assert settings.BASE_URL + reverse("unsubscription_start") in email.body


@pytest.mark.parametrize(
    "quantity,batch_size,expected_patches",
    [
        (
            3,
            1,
            [1, 1, 1],
        ),
        (
            4,
            2,
            [2, 2],
        ),
        (
            5,
            2,
            [2, 2, 1],
        ),
    ],
)
def test_get_newsletter_email_batchs(quantity, batch_size, expected_patches):
    baker.make(User, _quantity=quantity)
    clients = [user.client for user in User.objects.all()]
    batches = newsletter_email_batchs(None, clients, batch_size)

    batch_index = 0
    for batch in batches:
        print(batch, batch_index, expected_patches[batch_index])
        assert len(batch) == expected_patches[batch_index]
        batch_index += 1


def test_send_newsletter_email():
    baker.make(User, _quantity=11)
    clients = [user.client for user in User.objects.all()]
    send_newsletter_email(clients, batch_size=2)
    assert len(mail.outbox) == 11
