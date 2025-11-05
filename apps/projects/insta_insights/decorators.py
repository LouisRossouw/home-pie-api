from functools import wraps
# from users.serializers import IsSuperUser
# from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse, OpenApiParameter, OpenApiTypes, OpenApiExample
from . import serializers

# TODO; Fix authentication - dont AllowAny


def decorator_accounts(view_func):
    """Custom decorator to combine multiple DRF decorators."""

    @api_view(['GET', 'POST'])
    @permission_classes([AllowAny])
    @authentication_classes([])
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def decorator_account_detail(view_func):
    """Custom decorator to combine multiple DRF decorators."""

    @api_view(['GET', 'PATCH', 'DELETE'])
    @permission_classes([AllowAny])
    @authentication_classes([])
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def decorator_overview(view_func):
    """Custom decorator to combine multiple DRF decorators."""
    @api_view(['GET'])
    @permission_classes([AllowAny])
    @authentication_classes([])
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def decorator_config(view_func):
    """Custom decorator with method-specific OpenAPI responses."""
    @extend_schema_view(
        get=extend_schema(
            tags=["Insta Insights"],
            summary="Get project config",
            description="Returns the app's recorded configuration.",
            responses={
                200: OpenApiResponse(response=serializers.ConfigSerializer, description="Current configuration"),
            },
        ),
        put=extend_schema(
            tags=["Insta Insights"],
            summary="Update project config",
            description="Updates the configuration. Returns no content on success.",
            request=serializers.ConfigSerializer,
            responses={
                204: OpenApiResponse(description="Config updated successfully (no content)"),
            },
        ),
    )
    @api_view(["GET", "PUT"])
    @permission_classes([AllowAny])
    @authentication_classes([])
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)

    return _wrapped_view
