

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from oauth2_provider.models import AccessToken, RefreshToken
from drf_social_oauth2.views import TokenView as DRFSocialTokenView
from drf_spectacular.utils import extend_schema

from apps.core.user.models import User, LoginKey

from shared.utils.printouts.views.printout_users import printout_CustomUserCreate

from .decorators import complete_login_key_schema, poll_loginkey_view, create_loginkey_view
from .utils import get_access_expires_in, is_refresh_expired, issue_tokens
from .serializers import CustomUserSerializer, CustomTokenSerializer, CustomTokenRequestSerializer, CustomTokenResponseSerializer
from django.shortcuts import render, redirect
from django.conf import settings


F = str(__name__)
CUC = "CustomUserCreate"


class CustomTokenView(DRFSocialTokenView):
    """ Sign in with the manual auth """
    @extend_schema(
        summary="OAuth2 Token",
        description="Obtain an access token using username/password or refresh token.",
        request=CustomTokenRequestSerializer,
        responses={200: CustomTokenResponseSerializer},
    )
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            token_data = response.data
            access_token = token_data.get('access_token')
            if access_token:
                try:
                    token_obj = AccessToken.objects.get(token=access_token)
                    custom_response_data = CustomTokenSerializer(token_obj).data  # nopep8
                    custom_response_data.update(token_data)

                    return Response(custom_response_data)
                except AccessToken.DoesNotExist:
                    return Response({'error': 'Token not found'}, status=404)
        return response


class CustomUserCreate(APIView):
    """ Create account """

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, format='json'):
        data = request.data

        email = data.get("email", "").lower()
        username = data.get("username", "").lower()

        serializer = CustomUserSerializer(data=request.data)

        if serializer.is_valid():
            error = False
            email_exists = User.objects.filter(email=email).exists()
            username_exists = User.objects.filter(
                username=username).exists()

            if email_exists:
                error = {'email': 'Email already being used'}
            if username_exists:
                error = {'username': 'Username already being used'}
            if username_exists and email_exists:
                error = {
                    'email': 'Email already being used',
                    'username': 'Username already being used'
                }

            if error == False:
                user = serializer.save()
                printout_CustomUserCreate(F, CUC, user)
                if user:
                    json = serializer.data
                    json['user_id'] = user.id

                    return Response(json, status=status.HTTP_201_CREATED)

            else:
                print('Error:', error)
                return Response(error, status=status.HTTP_409_CONFLICT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@create_loginkey_view
class CreateLoginView(APIView):
    def post(self, request):
        login_key = LoginKey.objects.create()
        return Response({"loginKey": str(login_key.key)}, status=status.HTTP_201_CREATED)


@poll_loginkey_view
class PollLoginKeyView(RetrieveAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        key_str = kwargs["key"]

        if not key_str:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            login_key = LoginKey.objects.get(key=key_str)
        except LoginKey.DoesNotExist:
            return Response({"status": "invalid"}, status=status.HTTP_200_OK)

        if login_key.is_expired():
            login_key.delete()
            return Response({"status": "expired"}, status=status.HTTP_200_OK)

        if login_key.user:
            refresh_token = RefreshToken.objects.filter(
                user=login_key.user).last()

            if refresh_token:
                access_token = refresh_token.access_token
                is_expired = access_token.is_expired() if access_token else True
                if refresh_token.revoked or is_refresh_expired(refresh_token) or is_expired:
                    access_token, refresh_token = issue_tokens(login_key.user)
            else:
                access_token, refresh_token = issue_tokens(login_key.user)

            application = refresh_token.application  # Manual or Google auth type
            expires = access_token.expires
            expires_in = get_access_expires_in(access_token)

            custom_response_data = CustomTokenSerializer(access_token).data

            token_data = {
                "access_token": access_token.token,
                "refresh_token": refresh_token.token,
                "application": str(application),
                "user": custom_response_data['user'],
                "expires_in": expires_in,
                "expires": expires,
                "scope": custom_response_data['scope']
            }

            login_key.delete()
            return Response(token_data)

        return Response({"status": "pending"}, status=status.HTTP_200_OK)


class TestAuthView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "ok": True,
            "user": request.user.username,
            "auth": str(request.auth)
        })


@complete_login_key_schema
class CompleteLoginWithKeyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        key_str = request.query_params.get("loginKey")
        if not key_str:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            login_key = LoginKey.objects.get(key=key_str)
        except LoginKey.DoesNotExist:
            return Response({"status": "invalid"}, status=status.HTTP_200_OK)

        if login_key.is_expired():
            login_key.delete()
            return Response({"status": "expired"}, status=status.HTTP_200_OK)

        login_key.user = request.user
        login_key.save()

        return Response({"status": "complete"}, status=status.HTTP_201_CREATED)


# Removed @login_required to manually handle addAccount intent
def auth_app(request):
    import urllib.parse
    from django.contrib.auth import logout
    from django.shortcuts import resolve_url

    add_account = request.GET.get('addAccount') == 'true'

    if add_account:
        if request.user.is_authenticated:
            logout(request)

        params = request.GET.copy()
        params.pop('addAccount', None)
        next_url = request.path + '?' + urllib.parse.urlencode(params)

        login_url = resolve_url(settings.LOGIN_URL)
        return redirect(f"{login_url}?next={urllib.parse.quote(next_url)}")

    if not request.user.is_authenticated:
        login_url = resolve_url(settings.LOGIN_URL)
        next_url = request.get_full_path()
        return redirect(f"{login_url}?next={urllib.parse.quote(next_url)}")

    login_key_str = request.GET.get('loginKey')
    if not login_key_str:
        return render(request, 'user/auth_app.html', {'success': False})

    try:
        login_key = LoginKey.objects.get(key=login_key_str)
        if login_key.is_expired():
            return render(request, 'user/auth_app.html', {'success': False, 'error': 'Key expired'})

        # Associate the user with the key
        login_key.user = request.user
        login_key.save()

        is_dev = getattr(settings, 'DEV', True)
        protocol = f"homepie{'-dev' if is_dev else ''}"

        return render(request, 'user/auth_app.html', {
            'success': True,
            'protocol': protocol
        })
    except (LoginKey.DoesNotExist, ValueError):
        return render(request, 'user/auth_app.html', {'success': False, 'error': 'Invalid key'})
