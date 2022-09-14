import uuid

from django.db import models


class Subscriber(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    subscribed = models.BooleanField(default=False)
