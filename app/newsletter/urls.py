from django.urls import path

from newsletter.api import confirm_subscription, subscribe

urlpatterns = [
    path("subscription/start", subscribe, name="subscription_start"),
    path(
        "subscription/confirm/<secret_code>",
        confirm_subscription,
        name="subscription_confirm",
    ),
]
