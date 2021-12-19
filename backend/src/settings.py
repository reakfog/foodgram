import os

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = int(os.environ.get("DEBUG", default=0))

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", default=["*"])

INSTALLED_APPS = [
    # first-party apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.auth.hashers',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # third-party apps
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'drf_yasg',
    'colorfield',
    'djoser',
    # local apps
    'users',
    'recipes',
    'api',
]

MIDDLEWARE = [
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'src.urls'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
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
            ],
        },
    },
]

WSGI_APPLICATION = 'src.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': os.environ.get(
            'DB_ENGINE', default="django.db.backends.postgresql"),
        'NAME': os.environ.get(
            'DB_NAME', default="postgres"),
        'USER': os.environ.get(
            'POSTGRES_USER', default="postgres"),
        'PASSWORD': os.environ.get(
            'POSTGRES_PASSWORD', default="postgres"),
        'HOST': os.environ.get(
            'DB_HOST', default="db"),
        'PORT': os.environ.get(
            'DB_PORT', default="5432"),
    }
}

AUTH_USER_MODEL = 'users.User'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # noqa: E501
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # noqa: E501
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # noqa: E501
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # noqa: E501
    },
]


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

DJOSER = {
    'SERIALIZERS': {
        'user': 'api.serializers.UserSerializer',
        'current_user': 'api.serializers.UserSerializer',
        'user_create': 'api.serializers.CustomUserCreateSerializer',
        'token_create': 'api.serializers.CustomTokenCreateSerializer',
    },
    'PERMISSIONS': {
        'user_list': ('rest_framework.permissions.AllowAny',),
        'user': ('rest_framework.permissions.AllowAny',)
    },
    'HIDE_USERS': False,
    'LOGIN_FIELD': 'email',
}

LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

LANGUAGE_CODE = os.environ.get("LANGUAGE_CODE", default='en')

TIME_ZONE = os.environ.get("TIME_ZONE", default='Europe/Moscow')

USE_I18N = True

USE_L10N = True

USE_TZ = True
