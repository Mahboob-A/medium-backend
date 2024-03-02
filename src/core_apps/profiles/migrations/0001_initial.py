# Generated by Django 4.1.7 on 2024-03-02 06:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
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
                    "profile_photo",
                    models.ImageField(
                        default="/default_user_image/user-image.jpg",
                        upload_to="",
                        verbose_name="Profile Photo",
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[("M", "Male"), ("F", "Female"), ("O", "Other")],
                        default="M",
                        max_length=3,
                        verbose_name="Gender",
                    ),
                ),
                (
                    "phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        default="+918513998991",
                        max_length=20,
                        region=None,
                        verbose_name="Phone Number",
                    ),
                ),
                (
                    "about_me",
                    models.TextField(
                        default="Say something about yourself", verbose_name="About Me"
                    ),
                ),
                (
                    "country",
                    django_countries.fields.CountryField(
                        blank=True, default="IN", max_length=2, verbose_name="Country"
                    ),
                ),
                (
                    "city",
                    models.CharField(
                        blank=True,
                        default="Kolkata",
                        max_length=30,
                        verbose_name="City",
                    ),
                ),
                (
                    "twitter_handle",
                    models.CharField(
                        blank=True, max_length=25, verbose_name="Twitter/X Handle"
                    ),
                ),
                (
                    "followers",
                    models.ManyToManyField(
                        blank=True, related_name="following", to="profiles.profile"
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at", "-updated_at"],
                "abstract": False,
            },
        ),
    ]
