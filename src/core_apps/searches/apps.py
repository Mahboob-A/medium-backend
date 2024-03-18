from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SearchesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core_apps.searches"
    verbose_name = _("Search")
    verbose_name_plural = _("Searches")
