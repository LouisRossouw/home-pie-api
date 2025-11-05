
from datetime import timedelta

from django.utils import timezone
from django.conf import settings

from oauth2_provider.models import AccessToken, RefreshToken
from oauth2_provider.models import AccessToken, RefreshToken


def is_refresh_expired(refresh_token: RefreshToken) -> bool:
    expire_seconds = getattr(settings, "OAUTH2_PROVIDER", {}).get(
        "REFRESH_TOKEN_EXPIRE_SECONDS")
    if expire_seconds is None:
        return False  # never expires
    return refresh_token.created + timedelta(seconds=expire_seconds) < timezone.now()


def get_access_expires_in(access_token: AccessToken):
    now = timezone.now()
    return int((access_token.expires - now).total_seconds())


# # Generate new access tokens and refresh tokens if needed. ( Not in use yet )
# def issue_tokens(user: "User"):

#     # TODO; Pick either manual or google for the application.

#     app = Application.objects.get(name="Manual")

#     expires = timezone.now() + \
#         timedelta(
#             seconds=settings.OAUTH2_PROVIDER['ACCESS_TOKEN_EXPIRE_SECONDS'])

#     access_token = AccessToken.objects.create(
#         token=secrets.token_urlsafe(32),
#         scope="read write",
#         application=app,
#         expires=expires,
#         user=user,
#     )

#     refresh_token = RefreshToken.objects.create(
#         token=secrets.token_urlsafe(32),
#         access_token=access_token,
#         application=app,
#         user=user,
#     )

#     return {"access": access_token.token, "refresh": refresh_token.token}
