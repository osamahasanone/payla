import uuid

from django.db import models


class Client(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)
    subscribed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class SubscriptionAttempt(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    secret_code = models.CharField(max_length=25, unique=True)
    valid_from = models.DateTimeField(auto_now_add=True)
    valid_to = models.DateTimeField()
    succeed_at = models.BooleanField(null=True, blank= True)

    def _str__(self):
        return f"{self.client} - {self.secret_code}"