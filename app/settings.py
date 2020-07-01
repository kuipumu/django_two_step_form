"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import environ
import django_heroku
import dj_database_url
from django.urls import reverse_lazy
from django.core.management.utils import get_random_secret_key
from django.utils.translation import gettext_lazy as _

# Environ settings.
env = environ.Env(
    DEBUG=(bool, False),
    HEROKU=(bool, False)
)
# Reading .env file
environ.Env.read_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

# Boolean to set if is running under Heroku.
HEROKU = env('HEROKU')

ALLOWED_HOSTS = ['*']

# Admin users.

ADMINS = [x.split(':') for x in env.list('DJANGO_ADMINS')]

EMAIL_CONFIG = env.email_url(
    'EMAIL_URL', default='smtp://user@:password@localhost:25')

vars().update(EMAIL_CONFIG)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'formtools',
    'phonenumber_field',
    'crispy_forms',
    'captcha',
    'django_registration',
    'user'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': env.db()
}

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

# Custom User Model
# See https://docs.djangoproject.com/en/3.0/ref/settings/#auth-user-model

AUTH_USER_MODEL = 'user.CustomUser'

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

# Provide a lists of languages for the site.
LANGUAGES = (
    ('es', _('Spanish')),
)

# Add localization support.
USE_I18N = True

# Set calendar according to current locale.
USE_L10N = True

# Default language code.
LANGUAGE_CODE = env('LANGUAGE_CODE')

# Path to store locale files.
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

# Set default time zone.
TIME_ZONE = env('TIME_ZONE')

# Enable TZ for timezone.
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/assets/'
MEDIA_URL = '/media/'

# Static files folder
# https://docs.djangoproject.com/en/3.0/ref/settings/#staticfiles-dirs

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets/dist'),
)

# Static and Media root folders
# https://docs.djangoproject.com/en/3.0/ref/settings/#static-root
# https://docs.djangoproject.com/en/3.0/ref/settings/#media-root

STATIC_ROOT = os.path.join(BASE_DIR, "public/static")
MEDIA_ROOT = os.path.join(BASE_DIR, 'public/media')

# Authentication settings.

LOGIN_URL = reverse_lazy('login')
LOGIN_REDIRECT_URL = reverse_lazy('home')
LOGOUT_REDIRECT_URL = reverse_lazy('login')

# django-storages settings.

DEFAULT_FILE_STORAGE = 'storages.backends.dropbox.DropBoxStorage'
DROPBOX_OAUTH2_TOKEN = env('DROPBOX_OAUTH2_TOKEN')

# django-crispy-forms settings.

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# django-phonenumber_field settings.

PHONENUMBER_DB_FORMAT = 'NATIONAL'
PHONENUMBER_DEFAULT_REGION = env('PHONENUMBER_DEFAULT_REGION')

# django-recaptcha settings

if DEBUG:
    SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']
else:
    RECAPTCHA_PUBLIC_KEY = env('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = env('RECAPTCHA_PRIVATE_KEY')

# Company settings.

COMPANY_NAME = env('COMPANY_NAME')

# django-heroku settings.

django_heroku.settings(locals())