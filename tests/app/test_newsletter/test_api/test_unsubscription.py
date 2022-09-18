import arrow
import pytest
from django.test import override_settings
from freezegun.api import freeze_time
from model_bakery import baker

from newsletter.models import UnsubscriptionAttempt

pytestmark = pytest.mark.django_db


def test_start_unsubscription_success(subscribed_api_client):
    # Action
    response = subscribed_api_client.get("/newsletter/unsubscription/start")
    # Assert
    attempt = UnsubscriptionAttempt.objects.first()
    assert response.status_code == 200
    assert response.json() == {
        "confirmation_url": attempt.confirmation_url,
        "valid_to": attempt.valid_to.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    # other assertions (sending email and updating the DB) are already covered in testing services


def test_start_unsubscription_fails_when_already_unsubscribed(unsubscribed_api_client):
    response = unsubscribed_api_client.get("/newsletter/unsubscription/start")

    assert response.json() == {
        "error": {
            "status_code": 409,
            "message": "Request conflict",
            "details": {"detail": "You are not a subscriber"},
        }
    }


def test_confirm_unsubscription_success(subscribed_client, subscribed_api_client):
    attempt = baker.make(
        UnsubscriptionAttempt,
        client=subscribed_client,
        confirmed_at=None,
    )

    response = subscribed_api_client.get(
        f"/newsletter/unsubscription/confirm/{attempt.secret_code}"
    )

    assert response.status_code == 200
    # other assertions (updating the DB) are already covered in testing services


def test_confirm_unsubscription_fails_when_already_unsubscribed(
    unsubscribed_client, unsubscribed_api_client
):
    attempt = baker.make(
        UnsubscriptionAttempt,
        client=unsubscribed_client,
        confirmed_at=None,
    )

    response = unsubscribed_api_client.get(
        f"/newsletter/unsubscription/confirm/{attempt.secret_code}"
    )

    assert response.json() == {
        "error": {
            "status_code": 404,
            "message": "Nothing matches the given URI",
            "details": {
                "detail": "This link is either expired, not existed or you are not a subscriber"
            },
        }
    }


@override_settings(CONFIRMATION_LINK_VALIDITY_HOURS=1)
@freeze_time("2022-09-01 12:00:00", tz_offset=0)
def test_confirm_unsubscription_fails_when_attempt_is_expired(
    subscribed_client, subscribed_api_client
):
    attempt = baker.make(
        UnsubscriptionAttempt,
        client=subscribed_client,
        valid_from=arrow.utcnow().shift(hours=-24).datetime,
        confirmed_at=None,
    )

    response = subscribed_api_client.get(
        f"/newsletter/unsubscription/confirm/{attempt.secret_code}"
    )

    assert response.json() == {
        "error": {
            "status_code": 404,
            "message": "Nothing matches the given URI",
            "details": {
                "detail": "This link is either expired, not existed or you are not a subscriber"
            },
        }
    }


def test_confirm_unsubscription_fails_when_attempt_already_confirmed(
    subscribed_client, subscribed_api_client
):
    attempt = baker.make(
        UnsubscriptionAttempt,
        client=subscribed_client,
        valid_from=arrow.utcnow().shift(days=-1).datetime,
        confirmed_at=arrow.utcnow().datetime,
    )

    response = subscribed_api_client.get(
        f"/newsletter/unsubscription/confirm/{attempt.secret_code}"
    )

    assert response.json() == {
        "error": {
            "status_code": 404,
            "message": "Nothing matches the given URI",
            "details": {
                "detail": "This link is either expired, not existed or you are not a subscriber"
            },
        }
    }
