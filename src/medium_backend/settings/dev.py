

from .base import * # noqa 
from .base import env 

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = "django-insecure-=cypvt)o+f&2)8ah#!9xp%k7a7536(7lb4b$&0hsp!h!4y-7+r"

SECRET_KEY = env("DJANGO_SECRET_KEY", default="zE6EsmoLRWzrlsrsh2E2kWZqYetOpOzGd6hHeD4xQcQFSE23wKk",)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CSRF_TRUSTED_ORIGINS = ["http://localhost:8000"]

ALLOWED_HOSTS = ['3.7.42.121']


# EMAIL BACKEND # 
EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
EMAIL_HOST = env("EMAIL_HOST", default="mailhog")
DOMAIN = env("EMAIL_DOMAIN")
EMAIL_PORT = env("EMAIL_PORT")
DEFAULT_FROM_EMAIL = "iammahboob.a@gmail.com"
SITE_NAME = "Medium Backend"

