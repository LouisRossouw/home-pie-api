from django.contrib import admin
from django.urls import path, include
import main.views as main
from django.shortcuts import redirect
import django.contrib.auth.views as auth_views
from rest_framework.routers import DefaultRouter
from apps.core.user.views import (
    CustomUserCreate, 
    CustomTokenView, 
    CreateLoginView, 
    CompleteLoginWithKeyView, 
    PollLoginKeyView, 
    auth_app,
    TestAuthView
)

from apps.services.gengen import views as gen_gen
from apps.projects.insta_insights import views as insta_insights
from apps.projects.yt_insights import views as yt_insights
from apps.projects.time_in_progress import views as time_in_progress
from apps.services.mr_ping_ping import views as ping_ping
from apps.other.finances.views import FinanceSettingViewSet, FinanceRecordViewSet

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

router = DefaultRouter()
router.register(r'api/finances/settings', FinanceSettingViewSet, basename='finance-settings')
router.register(r'api/finances/records', FinanceRecordViewSet, basename='finance-records')

urlpatterns = [
    # ** Admin
    path('', lambda request: redirect('admin/')),
    path('admin/', admin.site.urls),

    # schema & Swagger & Redoc
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("api/docs/swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),

    # Router urls
    path('', include(router.urls)),

    # ** Server / API
    path('api/stats', main.stats, name='stats'),
    path('api/health', main.health, name='health'),
    path('api/test', main.test_view, name='test'),

    # ** User Management: Manual signup + Oauth with google
    path('auth/', include('drf_social_oauth2.urls', namespace='drf')),
    path('api/sign-up', CustomUserCreate.as_view(), name='user-create'),
    path('auth/login-manual', CustomTokenView.as_view(), name='login-manual'),

    # Electron Desktop app.
    path('auth/auth-app', auth_app, name='auth-app'),
    path('auth/login-key', CreateLoginView.as_view(), name='login-key'),
    path("auth/login-key/<uuid:key>", PollLoginKeyView.as_view(), name="login-key-poll"),
    path("auth/login-key/complete", CompleteLoginWithKeyView.as_view(), name="login-complete"),
    path("auth/test", TestAuthView.as_view(), name="test-auth"),
    path('login/', auth_views.LoginView.as_view(), name='login'),

    # ** Projects
    path('api/time-in-progress/config', time_in_progress.config),
    path('api/time-in-progress/overview', time_in_progress.overview),
    path('api/time-in-progress/<str:platform>/data', time_in_progress.platform_data),

    path('api/insta-insights/config', insta_insights.config),
    path('api/insta-insights/overview', insta_insights.overview),
    path('api/insta-insights/accounts', insta_insights.accounts),
    path('api/insta-insights/accounts/<str:account_name>', insta_insights.account_detail),
    
    path('api/yt-insights/config', yt_insights.config),
    path('api/yt-insights/overview', yt_insights.overview),
    path('api/yt-insights/accounts', yt_insights.accounts),
    path('api/yt-insights/accounts/<str:account_name>', yt_insights.account_detail),

    # ** GenGen
    path('api/gengen/start', gen_gen.start_gengen),
    path('api/gengen/check-progress', gen_gen.check_progress),

    # ** Mr-Ping-ing
    path('api/mr-ping-ping/config', ping_ping.pingping_config),
    path('api/mr-ping-ping/status', ping_ping.pingping_status),
    path('api/mr-ping-ping/apps/configs', ping_ping.apps_config),
    path('api/mr-ping-ping/apps/configs/<str:app_name>', ping_ping.app_config),
    path('api/mr-ping-ping/apps/status', ping_ping.apps_status),
    path('api/mr-ping-ping/apps/status/<str:app_name>', ping_ping.app_status),
    path('api/mr-ping-ping/apps/data/<str:app_name>', ping_ping.app_recorded_data),
]
