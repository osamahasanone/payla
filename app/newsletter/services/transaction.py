import secrets

from newsletter.models import ClientTransaction

SECRET_NBYTES = 4  # how many bytes a secret should be


def get_secret(model: ClientTransaction, bytes: int = SECRET_NBYTES) -> str:
    secret = secrets.token_urlsafe(bytes)
    # token_urlsafe function returns unique secrets, but to be more strict:
    if not model.objects.filter(secret_code=secret).exists():
        return secret
    get_secret()
