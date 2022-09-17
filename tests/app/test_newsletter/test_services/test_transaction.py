import pytest

from newsletter.models import SubscriptionAttempt, UnsubscriptionAttempt
from newsletter.services.transaction import get_secret

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize("model", [SubscriptionAttempt, UnsubscriptionAttempt])
def test_get_secret_return_unique_values(model):
    test_size = 10  # tested with huge numbers, but set to 10 to keep the test fast
    secrets = []
    for _ in range(test_size):
        secrets.append(get_secret(model))
    assert len(set(secrets)) == test_size
