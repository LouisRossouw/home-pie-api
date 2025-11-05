from apps.core.user.models import User
from rest_framework import serializers
from oauth2_provider.models import AccessToken
from rest_framework.permissions import BasePermission


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'auth_type',
            'is_staff',
        )


class CustomTokenSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = AccessToken
        fields = ('expires', 'scope', 'user')


class CustomTokenRequestSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=False)
    client_id = serializers.CharField(required=False)
    auth_type = serializers.CharField(required=False)
    grant_type = serializers.CharField()


class CustomTokenResponseSerializer(CustomTokenSerializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    token_type = serializers.CharField()
    expires_in = serializers.IntegerField()

    class Meta(CustomTokenSerializer.Meta):
        fields = CustomTokenSerializer.Meta.fields + (
            'access_token',
            'refresh_token',
            'token_type',
            'expires_in',
        )


class IsSuperUser(BasePermission):
    """ Custom permission to only allow superusers to access the endpoint. """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_superuser


class CreateLoginKeySerializer(serializers.Serializer):
    login_key = serializers.CharField()


class CompleteLoginKeySerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        choices=["complete", "invalid", "expired"],
        help_text="Status of the login key process"
    )


class PollLoginKeyTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    application = serializers.CharField()
    user = CustomTokenSerializer()
    expires_in = serializers.IntegerField()
    expires = serializers.DateTimeField()
    scope = serializers.CharField()
