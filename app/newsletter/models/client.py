import uuid

from django.conf import settings
from django.db import models


class ClientQuerySet(models.QuerySet):
    def subscribed(self) -> "ClientQuerySet":
        return self.filter(subscribed=True)


class Client(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subscribed = models.BooleanField(default=False, db_index=True)

    objects = ClientQuerySet.as_manager()

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"
