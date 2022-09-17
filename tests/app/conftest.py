import pytest
from model_bakery import baker
from rest_framework.test import APIClient

from core.models import User


@pytest.fixture
def unsubscribed_client():
    user = baker.make(User)
    return user.client


@pytest.fixture
def unsubscribed_api_client(unsubscribed_client):
    client = APIClient()
    client.force_authenticate(user=unsubscribed_client.user)
    return client


@pytest.fixture
def subscribed_client():
    user = baker.make(User)
    user.client.subscribed = True
    user.client.save()
    return user.client


@pytest.fixture
def subscribed_api_client(subscribed_client):
    client = APIClient()
    client.force_authenticate(user=subscribed_client.user)
    return client
