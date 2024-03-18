from django.contrib.admin import ModelAdmin, register

from core_apps.ratings.models import Ratings


@register(Ratings)
class RatingAdmin(ModelAdmin):
    list_display = [
        "id",
        "article",
        "user",
        "rating",
        "review",
        "created_at",
        "updated_at",
    ]
