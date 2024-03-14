# Generated by Django 4.1.7 on 2024-03-12 11:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("articles", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Ratings",
            fields=[
                (
                    "pkid",
                    models.BigAutoField(
                        editable=False, primary_key=True, serialize=False
                    ),
                ),
                (
                    "id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "rating",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (1, "Poor"),
                            (2, "Fair"),
                            (3, "Good"),
                            (4, "Very Good"),
                            (5, "Excellent"),
                        ],
                        verbose_name="Article Rating",
                    ),
                ),
                ("review", models.TextField(blank=True, verbose_name="Article Review")),
                (
                    "article",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ratings",
                        to="articles.article",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="users_rating",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Rating",
                "verbose_name_plural": "Ratings",
                "unique_together": {("article", "user")},
            },
        ),
    ]