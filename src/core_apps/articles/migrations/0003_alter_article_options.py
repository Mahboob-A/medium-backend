# Generated by Django 4.1.7 on 2024-03-18 07:54

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("articles", "0002_alter_articleviews_user_clap_article_clapps"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="article",
            options={
                "ordering": ["-created_at"],
                "verbose_name": "Article",
                "verbose_name_plural": "Articles",
            },
        ),
    ]
