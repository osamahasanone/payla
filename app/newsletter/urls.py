from django.urls import path

from newsletter.api import (
    confirm_user_subscription,
    confirm_user_unsubscription,
    subscribe,
    unsubscribe,
)

urlpatterns = [
    path("subscription/start", subscribe, name="subscription_start"),
    path(
        "subscription/confirm/<secret_code>",
        confirm_user_subscription,
        name="subscription_confirm",
    ),
    path("unsubscription/start", unsubscribe, name="unsubscription_start"),
    path(
        "unsubscription/confirm/<secret_code>",
        confirm_user_unsubscription,
        name="unsubscription_confirm",
    ),
]
