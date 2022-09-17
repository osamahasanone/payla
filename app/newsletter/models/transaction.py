import uuid
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone

from newsletter.models import Client


class ClientTransactionQuerySet(models.QuerySet):
    def outdated(self) -> "ClientTransaction":
        return self.filter(valid_to__lte=timezone.now(), confirmed_at__isnull=True)


class ClientTransaction(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    secret_code = models.CharField(max_length=25, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    confirmed_at = models.DateTimeField(null=True, blank=True)

    objects = ClientTransactionQuerySet.as_manager()

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f"{self.client} - {self.secret_code} - until {self.valid_to} "

    def save(self, *args, **kwargs):
        # because valid_from will be None here if we use auto_now_add=True
        if not self.valid_from:
            self.valid_from = timezone.now()
        self.valid_to = self.valid_from + timedelta(
            hours=settings.CONFIRMATION_LINK_VALIDITY_HOURS
        )
        super(ClientTransaction, self).save(*args, **kwargs)


class SubscriptionAttempt(ClientTransaction):
    @property
    def confirmation_url(self):
        return settings.BASE_URL + reverse(
            "subscription_confirm", args=[self.secret_code]
        )


class UnsubscriptionAttempt(ClientTransaction):
    @property
    def confirmation_url(self):
        return settings.BASE_URL + reverse(
            "unsubscription_confirm", args=[self.secret_code]
        )
