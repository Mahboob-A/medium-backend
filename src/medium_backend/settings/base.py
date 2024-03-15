"""
Django settings for medium_backend project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
# 070224, Wednesday, 03.00 pm 


############################ Path and Env 

from pathlib import Path
from datetime import timedelta

import environ
env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.

# this effectively pointing to the SRC dir where the manage.py file is located. 
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
# print(ROOT_DIR)

# all the apps dir 
APP_DIR = ROOT_DIR / 'core_apps'

DEBUG = env.bool('DJANGO_DEBUG', False)

############################ 

# TODO remove the force script for normal application. this is being used as I am developing 
# the project in AWS EC2 instance. 
# Also remove the script in case of deployment. 
# this is for development only to access the dev project on EC2 server. 
#CHECK:  use this only when checking in local dev, not while creating docker containers. 



############################ Application Definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites", 
]

THIRD_PARTY_APPS = [
    "rest_framework", 
    "django_filters", 
    "django_countries", 
    "phonenumber_field", 
    "drf_yasg", 
    "corsheaders", 
    'djcelery_email',
    'allauth', 
    'allauth.account', 
    'allauth.socialaccount', 
    'dj_rest_auth', 
    'dj_rest_auth.registration', 
    'rest_framework.authtoken', 
    'taggit', 
    
]

LOCAL_APPS = [
    "core_apps.profiles", 
    "core_apps.common", 
    "core_apps.users", 
    'core_apps.articles', 
    'core_apps.ratings', 
    'core_apps.bookmarks', 
]

# installed apps 
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS 

###########################





############################ Middleware and Templates and Root URL Conf 

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware", # cors middleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "medium_backend.urls"

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

############################ 





############################ Server, Database, Password Hashers(argon2-cffi) and Django Password Validators 

WSGI_APPLICATION = "medium_backend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# TODO dev database set to postgres database in docker container build 
'''
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ROOT_DIR / "db.sqlite3",  # mydatabase 
    }
}
'''

# TODO prod Database 
DATABASES = {
    "default": env.db("DATABASE_URL")
}


# Password Hashers (argon2-cffi)
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

############################ 






############################ Timezone Static and Meidafiles  

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True

SITE_ID = 1 

ADMIN_URL = "adminpanel/" # make it not guessable    



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "/staticfiles/"
STATIC_ROOT = str(ROOT_DIR / "staticfiles")

MEDIA_URL = "/mediafiles/"
MEDIA_ROOT = str(ROOT_DIR / "mediafiles")

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


############################ 

############################ CELERY CONFIG 
CELERY_BROKER_URL = env("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTECT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_RESULT_BACKEND_MAX_RETRIES = 15
CELERY_TASK_SEND_SENT_EVENT = True 

if USE_TZ: 
    CELERY_TIMEZONE = TIME_ZONE




############################ CORS And Others 

CORS_URLS_REGEX = r"^api/.*$"

AUTH_USER_MODEL = "users.CustomUser"

''' API and AUTH SETTINGS '''

#   Rest Framework Settings 
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES" : [
        "dj_rest_auth.jwt_auth.JWTCookieAuthentication", 
    ], 
    "DEFAULT_PERMISSION_CLASSES" : [
        "rest_framework.permissions.IsAuthenticated", 
    ], 
    "DEFAULT_FILTER_BACKENDS" : [
        "django_filters.rest_framework.DjangoFilterBackend"
    ]
}

# DRF Simple JWT Settings 
SIMPLE_JWT = {
    "AUTH_HEADER_TYPES" : ("Bearer", ), 
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=25), 
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1), 
    "ROTATE_REFRESH_TOKENS": True, 
    "SIGNING_KEY": env("SIGNING_KEY"), 
    "USER_ID_FIELD": "id", 
    "USER_IF_CLAIM": "user_id", 
}

# DJ Rest AUTH Settings 
REST_AUTH = {
    "USE_JWT": True, 
    "JWT_AUTH_COOKIE": "medium-backend-access-token", 
    "JWT_AUTH_REFRESH_COOKIE": "medium-backend-refresh-token", 
    "REGISTER_SERIALIZER": "core_apps.users.serializers.CustomRegisterSerializer", 
}

# Auth Backend 
AUTHENTICATION_BACKENDS = [
    "allauth.account.auth_backends.AuthenticationBackend", 
    "django.contrib.auth.backends.ModelBackend", 
]

# Other allauth Auth Settings 
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_CONFIRM_EMAIL_ON_GET = True 
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_USER_MODEL_USERNAME_FIELD = None 
ACCOUNT_USERNAME_REQUIRED = False 

########################################################


LOGGING = {
    "version": 1, 
    "disable_existing_loggers": False, 
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(name)-12s %(asctime)s %(module)s  %(process)d %(thread)d %(message)s "
            }
    },
    "handlers": {
        "console": {
            "level": "DEBUG", 
            "class": "logging.StreamHandler", 
            "formatter": "verbose", 
        }
    },
    "root": {
        "level": "INFO", 
        "handlers": ["console"], 
    },
    
    # uncomment for django database query logm
    # 'loggers': {
    #     'django.db': {
    #         'level': 'DEBUG',
    #         'handlers': ['console'],
    #     }
    # }
}





