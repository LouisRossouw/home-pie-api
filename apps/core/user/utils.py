import secrets
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from oauth2_provider.models import AccessToken, RefreshToken, Application

def is_refresh_expired(refresh_token: RefreshToken) -> bool:
    expire_seconds = getattr(settings, "OAUTH2_PROVIDER", {}).get(
        "REFRESH_TOKEN_EXPIRE_SECONDS")
    if expire_seconds is None:
        return False  # never expires
    return refresh_token.created + timedelta(seconds=expire_seconds) < timezone.now()

def get_access_expires_in(access_token: AccessToken):
    now = timezone.now()
    return int((access_token.expires - now).total_seconds())

def issue_tokens(user):
    # Get any application. Usually we want the one intended for this app.
    app = Application.objects.first()
    if not app:
        # Create a default application if none exists
        app = Application.objects.create(
            name="Manual",
            user=user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
        )

    expires_in = getattr(settings, "OAUTH2_PROVIDER", {}).get(
        "ACCESS_TOKEN_EXPIRE_SECONDS", 36000)
    expires = timezone.now() + timedelta(seconds=expires_in)

    access_token = AccessToken.objects.create(
        user=user,
        scope="read write",
        expires=expires,
        token=secrets.token_hex(32),
        application=app
    )

    refresh_token = RefreshToken.objects.create(
        user=user,
        token=secrets.token_hex(32),
        access_token=access_token,
        application=app
    )

    return access_token, refresh_token
