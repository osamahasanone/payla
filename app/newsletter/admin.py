from django.contrib import admin

from newsletter.models import Client, SubscriptionAttempt, UnsubscriptionAttempt

# This is just for making QA easier


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ["user", "subscribed"]
    search_fields = ["user"]
    ordering = ["-id"]
    list_per_page = 25


@admin.register(SubscriptionAttempt, UnsubscriptionAttempt)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        "secret_code",
        "confirmation_url",
        "client",
        "valid_from",
        "valid_to",
        "confirmed_at",
    ]
    search_fields = ["secret_code"]
    ordering = ["-id"]
    list_per_page = 25
