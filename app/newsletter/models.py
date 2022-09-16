import uuid

from django.conf import settings
from django.db import models


class Client(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subscribed = models.BooleanField(default=False, db_index=True)

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"


class SubscriptionAttempt(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    secret_code = models.CharField(max_length=25, unique=True)
    valid_from = models.DateTimeField(auto_now_add=True)
    valid_to = models.DateTimeField()
    confirmed_at = models.DateTimeField(null=True, blank=True)

    def _str__(self):
        return f"{self.client} - {self.secret_code}"
