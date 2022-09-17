from django.conf import settings
from django.core import mail
from django.template.loader import render_to_string
from django.urls import reverse


def compose_single_newsletter_email(connection, client):
    return mail.EmailMessage(
        settings.NEWSLETTER_EMAIL_SUBJECT,
        render_to_string(
            settings.NEWSLETTER_EMAIL_EMAIL_TEMPLATE,
            {
                "name": client,
                "url": settings.BASE_URL + reverse("unsubscription_start"),
            },
        ),
        settings.EMAIL_HOST_USER,
        [client.user.email],
        connection=connection,
    )


def newsletter_email_batchs(connection, clients, batch_size):
    emails = []
    for client in clients:
        emails.append(compose_single_newsletter_email(connection, client))
        if len(emails) == batch_size:
            yield emails
            emails = []
    # for last batch, if there are emails
    if emails:
        yield emails


def send_newsletter_email(clients, batch_size=settings.NEWSLETTER_EMAIL_BATCH_SIZE):
    connection = mail.get_connection()
    connection.open()

    for batch in newsletter_email_batchs(connection, clients, batch_size):
        print("=" * 30)
        print(f"sending batch of {len(batch)} email(s)")
        print("=" * 30)
        connection.send_messages(batch)

    connection.close()
