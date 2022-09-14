from django.contrib import admin

from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ["email", "first_name", "last_name"]
    search_fields = ["id", "email", "first_name", "last_name" "subscribed"]
    ordering = ["id"]
    readonly_fields = ["id"]
    fields = ["id", "email", "first_name", "last_name", "subscribed"]
    list_per_page = 25
