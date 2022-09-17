from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from newsletter.models import Client, SubscriptionAttempt


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_client_for_new_user(sender, **kwargs):
    if kwargs["created"]:
        Client.objects.create(user=kwargs["instance"])


@receiver(post_save, sender=SubscriptionAttempt)
def send_confirmation_email_for_subscription_attempt(sender, **kwargs):
    attempt = kwargs["instance"]
    if kwargs["created"]:
        send_mail(
            settings.SUBSCRIPTION_CONFIRMATION_EMAIL_SUBJECT,
            render_to_string(
                settings.SUBSCRIPTION_CONFIRMATION_EMAIL_TEMPLATE,
                {"name": attempt.client, "url": attempt.confirmation_url},
            ),
            settings.EMAIL_HOST_USER,
            [attempt.client.user.email],
            fail_silently=False,
        )
