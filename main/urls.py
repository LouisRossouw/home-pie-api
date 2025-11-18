from django.contrib import admin
from django.urls import path
# from django.views.generic.base import RedirectView
from django.urls import path, include
import main.views as main
from django.shortcuts import redirect
from rest_framework.routers import DefaultRouter
from apps.core.user.views import CustomUserCreate, CustomTokenView, CreateLoginView, CompleteLoginWithKeyView, PollLoginKeyView
from apps.iot.inventory.views import CompartmentViewSet,  InventoryViewSet, PartViewSet, StorageUnitViewSet
from apps.services.gengen import views as gen_gen
from apps.projects.insta_insights import views as insta_insights
from apps.projects.time_in_progress import views as time_in_progress

from apps.services.mr_ping_ping import views as ping_ping

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


router = DefaultRouter()

# ** IOT Physical devices etc.
router.register(r"iot/inventory/storage-units", StorageUnitViewSet)
router.register(r"iot/inventory/compartments", CompartmentViewSet)
router.register(r"iot/inventory/parts", PartViewSet)
router.register(r"iot/inventory", InventoryViewSet)

urlpatterns = [
    # ** Admin
    #  path('', main.home_view, name='home'),
    path('', lambda request: redirect('admin/')),
    path('admin/', admin.site.urls),
    # ** ----

    path("api/", include(router.urls)),

    # schema & Swagger & Redoc
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc",),  # nopep8
    path("api/docs/swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui",),  # nopep8

    # ** Server / API
    path('api/stats', main.stats),
    path('api/health', main.health),
    path('api/test', main.test_view),
    # ** ----

    # ** User Management: Manual signup + Oauth with google
    path('auth/', include('drf_social_oauth2.urls', namespace='drf')),
    path('api/sign-up', CustomUserCreate.as_view(), name='user-create'),
    path('auth/login-manual', CustomTokenView.as_view(), name='login-manual'),

    # Electron Desktop app.
    path('auth/login-key', CreateLoginView.as_view(), name='login-key'),
    path("auth/login-key/<uuid:key>", PollLoginKeyView.as_view(), name="login-key-poll"),  # nopep8
    path("auth/login-key/complete", CompleteLoginWithKeyView.as_view(), name="login-complete"),  # nopep8
    # ** ----

    # ** Projects
    # - Projects; TimeInProgress
    path('api/time-in-progress/config', time_in_progress.config),
    path('api/time-in-progress/overview', time_in_progress.overview),
    path('api/time-in-progress/<str:platform>/data', time_in_progress.platform_data),  # nopep8

    # - Projects; InstaInsights
    path('api/insta-insights/config', insta_insights.config),
    path('api/insta-insights/overview', insta_insights.overview),
    path('api/insta-insights/accounts', insta_insights.accounts),
    path('api/insta-insights/accounts/<str:account_name>', insta_insights.account_detail),  # nopep8
    # ** ----

    # ** GenGen
    # - TimeInProgress
    path('api/gengen/start', gen_gen.start_gengen),
    path('api/gengen/check-progress', gen_gen.check_progress),  # nopep8
    # ** ----

    # ** Mr-Ping-ing
    path('api/mr-ping-ping/config', ping_ping.pingping_config),
    path('api/mr-ping-ping/status', ping_ping.pingping_status),

    # path('api/mr-ping-ping/apps', ping_ping.app_config),
    path('api/mr-ping-ping/apps/configs', ping_ping.apps_config),
    path('api/mr-ping-ping/apps/configs/<str:app_name>', ping_ping.app_config),
    path('api/mr-ping-ping/apps/status', ping_ping.apps_status),
    path('api/mr-ping-ping/apps/status/<str:app_name>', ping_ping.app_status),
    path('api/mr-ping-ping/apps/data/<str:app_name>', ping_ping.app_recorded_data),  # nopep8
    # ** ----
]
