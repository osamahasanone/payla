from django.contrib import admin

from .models import Subscriber


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ["email", "name"]
    search_fields = ["id", "email", "name", "subscribed"]
    ordering = ["id"]
    readonly_fields = ["id"]
    fields = ["id", "email", "name", "subscribed"]
    list_per_page = 25
