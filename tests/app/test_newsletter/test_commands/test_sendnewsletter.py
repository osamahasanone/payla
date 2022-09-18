from unittest import mock

import pytest
from django.core import mail
from django.core.management import call_command
from model_bakery import baker

from core.models import User
from newsletter.models import Client

pytestmark = pytest.mark.django_db


def test_send_newsletter_only_to_subscribed():
    # 50 subscribed clients
    baker.make(User, _quantity=50)
    Client.objects.update(subscribed=True)

    # 20 unsubscribed clients
    baker.make(User, _quantity=20)

    call_command("sendnewsletter")

    assert len(mail.outbox) == 50


@mock.patch("newsletter.management.commands.sendnewsletter.send_newsletter_email")
def test_send_newsletter_command_with_no_arguments(send_newsletter_email_mock):
    baker.make(User, _quantity=5)
    Client.objects.update(subscribed=True)

    call_command("sendnewsletter")

    # Just test calling with one argument, unit tests for send_newsletter_email already there
    send_newsletter_email_mock.assert_called_once_with(mock.ANY)


@mock.patch("newsletter.management.commands.sendnewsletter.send_newsletter_email")
def test_send_newsletter_command_with_batch_argument(send_newsletter_email_mock):
    baker.make(User, _quantity=5)
    Client.objects.update(subscribed=True)

    call_command("sendnewsletter", batch=2)

    # Just test calling with one argument, unit tests for send_newsletter_email already there
    send_newsletter_email_mock.assert_called_once_with(mock.ANY, 2)
