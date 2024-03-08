# Generated by Django 4.1.7 on 2024-03-08 10:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("profiles", "0006_alter_profile_profile_photo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="profile_photo",
            field=models.ImageField(
                default="default-user-image.jpg",
                upload_to="CustomUsers/ProfilePictures/",
                verbose_name="Profile Photo",
            ),
        ),
    ]
