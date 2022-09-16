from django.contrib import admin

from newsletter.models import Client, SubscriptionAttempt


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass


@admin.register(SubscriptionAttempt)
class SubscriptionAttemptAdmin(admin.ModelAdmin):
    pass
