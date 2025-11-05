from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from . import serializers


complete_login_key_schema = extend_schema(
    tags=["auth-desktop-app"],
    summary="Complete the loginKey (Desktop apps)",
    description="Assigns the user to the loginKey that was generated for the desktop app.",
    parameters=[
        OpenApiParameter(
            name="loginKey",
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.QUERY,
            required=True,
        ),
    ],
    responses={201: serializers.CompleteLoginKeySerializer},
)


poll_loginkey_view = extend_schema(
    tags=["auth-desktop-app"],
    summary="Poll for a loginKey (Desktop apps)",
    description="Checks the status of a loginKey and, if authenticated, returns tokens.",
    responses={200: serializers.PollLoginKeyTokenSerializer},
)


create_loginkey_view = extend_schema(
    tags=["auth-desktop-app"],
    summary="Creates a loginKey (Desktop apps)",
    description="Creates and returns a loginKey for the desktop app in order to complete the handshake. ",
    responses={200: serializers.CreateLoginKeySerializer},
)
