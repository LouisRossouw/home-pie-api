import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEV = True if os.getenv('APP_ENV') == "dev" else False
DEBUG = True if DEV else False

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS').split(",")

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',

    'drf_spectacular',  # generates the schema
    'drf_spectacular_sidecar',  # nopep8 # bundles Swagger UI & Redoc.

    # drf-social-oauth2
    'oauth2_provider',
    'social_django',
    'drf_social_oauth2',

    # Core
    'apps.core.user',

    # Services
    'apps.services.gengen',
    'apps.services.mr_ping_ping',

    # Projects
    'apps.projects.insta_insights',
    'apps.projects.time_in_progress',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # drf-social-oauth2
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    str(BASE_DIR) + "/main/static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    'DEFAULT_RENDERER_CLASSES': [
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
        'djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer',
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.AdminRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'drf_social_oauth2.authentication.SocialAuthentication',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
        'djangorestframework_camel_case.parser.CamelCaseFormParser',
        'djangorestframework_camel_case.parser.CamelCaseMultiPartParser',
    ),
}


AUTHENTICATION_BACKENDS = (
    # Others auth providers (e.g. Google, OpenId, etc)

    # Google  OAuth2
    'social_core.backends.google.GoogleOAuth2',

    # Manual login
    # drf_social_oauth2
    'drf_social_oauth2.backends.DjangoOAuth2',

    # Manual login
    # Django
    'django.contrib.auth.backends.ModelBackend',
)

# TODO; Not needing yet but nice to have in the future.
# Google configuration
# SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
# SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv(
#     'SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')

# SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
#     'https://www.googleapis.com/auth/userinfo.email',
#     'https://www.googleapis.com/auth/userinfo.profile',
# ]


PROJECT_NAME = "Home-Pie"
DEV_BASEURL = os.getenv('DJANGO_DEV_BASEURL')
PROD_BASEURL = os.getenv('DJANGO_PROD_BASEURL')
SERVER_API_URL = DEV_BASEURL if DEV else PROD_BASEURL


AUTH_USER_MODEL = "user.User"

# TELEGRAM
TELEGRAM_NOTIFICATIONS = True

# Mail Service
MAIL_DEV = False
# IF True, send to my sandbox mail for testing - else send to customer mail.
MAIL_DELIVERY_SANDBOX = False
MAIL_DELIVERY_SANDBOX_MAIL = os.getenv("SANDBOX_MAIL")

if MAIL_DEV == True:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = os.getenv("NAME_GMAIL_SMTP")
    EMAIL_HOST_PASSWORD = os.getenv("PASSWORD_GMAIL_SMTP")
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


# just print statements in color or not, should actually change this to logger!
PRINTOUTS = True if DEV else False
PRINTOUTS_FRM = 'RED'

# Open api
SPECTACULAR_SETTINGS = {
    "TITLE": "HomePie API",
    "DESCRIPTION": "API documentation",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,

    "COMPONENT_SPLIT_REQUEST": True,
    "SCHEMA_PATH_PREFIX": r"/api/v1",

    "SECURITY": [{"BearerAuth": []}],  # TODO; Why does this not work
    "COMPONENTS": {
        "securitySchemes": {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            }
        }
    },
    'CAMELIZE_NAMES': True,  # Changes urls from snake case to camel case.
    'POSTPROCESSING_HOOKS': [
        # Changes snake case to camel case in the return response
        'drf_spectacular.contrib.djangorestframework_camel_case.camelize_serializer_fields',
    ],
    # "SERVE_PERMISSIONS": ["rest_framework.permissions.IsAdminUser"],
    # "SERVE_AUTHENTICATION": [
    #     "rest_framework.authentication.BasicAuthentication"
    # ],
}


print("--")
print("Starting Server with config:")
print('IS_DEV:', DEV)
print('PROJECT_NAME:', PROJECT_NAME)
print("SERVER_URL:", SERVER_API_URL)

print('MAIL_DELIVERY_SANDBOX:', MAIL_DELIVERY_SANDBOX)
print("--")
