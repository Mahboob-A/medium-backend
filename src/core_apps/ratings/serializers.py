from rest_framework import serializers
from .models import Ratings


class RatingSerializer(serializers.ModelSerializer):
    article_title = serializers.CharField(source="article.title", read_only=True)
    article_id = serializers.UUIDField(source="article.id", read_only=True)
    writer_first_name = serializers.CharField(
        source="article.author.first_name", read_only=True
    )
    writer_last_name = serializers.CharField(
        source="article.author.last_name", read_only=True
    )
    user_first_name = serializers.CharField(source="user.first_name", read_only=True)
    user_last_name = serializers.CharField(source="user.last_name", read_only=True)

    class Meta:
        model = Ratings
        fields = [
            "id",
            "article_title",
            "article_id",
            "writer_first_name",
            "writer_last_name",
            "user_first_name",
            "user_last_name",
            "rating",
            "review",
        ]
