"""
Django settings for socialnet project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
from django.urls import reverse_lazy

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "tgo1!g&butvd&n0*_oi6han458-_%1^v$!0ja=-)pbsmge=yzb"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["mysite.com", "localhost:8000", "127.0.0.1", "503a384c.ngrok.io",]

# backends for authentication

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "account.authentication.EmailAuthBackend",
    "social_core.backends.facebook.FacebookOAuth2",
    "social_core.backends.google.GoogleOAuth2",
]

"""Settings for logging by Facebook account"""

SOCIAL_AUTH_FACEBOOK_KEY = (
    "188812629085947"  # Facebook app id (из кабинета разработчика)
)
SOCIAL_AUTH_FACEBOOK_SECRET = (
    "5b4e25ec043ac89f46bbcddcebf3d400"  # Facebook app secret (оттуда же)
)
SOCIAL_AUTH_FACEBOOK_SCOPE = [
    "email"
]  # параметры, которые запрашиваются у пользователя при попытке залогиниться

"""Settings for logging by Google account"""

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = "XXX"  # Google Consumer Key
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "XXX"  # Google Consumer Secret

# Application definition

INSTALLED_APPS = [
    "account.apps.AccountConfig",  # Added after creating app by "$ django-admin startapp account"
    "images.apps.ImagesConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "social_django",
    "sorl.thumbnail",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "socialnet.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "socialnet.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Redirect URLs

LOGIN_REDIRECT_URL = "dashboard"  # адрес куда полетит пользователь после логина, если не указана GET "next"
LOGIN_URL = "login"  # адрес который будет использоваться при необходимости залогиниться
LOGOUT_URL = "logout"


# SMTP-заглушка (настроить smtp как в прошлом проекте)

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# Media settings

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")   

# Other

ABSOLUTE_URL_OVERRIDES = { # Эта настройка добавляет метод get_absoluteл_url для всех моделей указанных в ней
    'auth.user': lambda u: reverse_lazy('user_detail', args=[u.username])
}
