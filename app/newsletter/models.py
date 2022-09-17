import uuid
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Client(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subscribed = models.BooleanField(default=False, db_index=True)

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"


class ClientTransaction(models.Model):
    secret_code = models.CharField(max_length=25, unique=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # because valid_from will be None here if we use auto_now_add=True
        self.valid_from = timezone.now()
        self.valid_to = self.valid_from + timedelta(
            hours=settings.CONFIRMATION_LINK_VALIDITY_HOURS
        )
        super(ClientTransaction, self).save(*args, **kwargs)


class SubscriptionAttempt(ClientTransaction):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f"{self.client} - {self.secret_code} - until {self.valid_to} "

    @property
    def confirmation_url(self):
        return settings.BASE_URL + reverse(
            "subscription_confirm", args=[self.secret_code]
        )
