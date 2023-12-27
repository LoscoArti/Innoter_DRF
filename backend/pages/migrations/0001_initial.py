# Generated by Django 5.0 on 2023-12-18 14:20

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("tags", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Page",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True)),
                ("user_id", models.UUIDField(null=True)),
                ("user_group_id", models.IntegerField(null=True)),
                ("image_url", models.URLField(blank=True)),
                ("is_blocked", models.BooleanField(default=False)),
                ("unblock_date", models.DateField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("tags", models.ManyToManyField(related_name="pages", to="tags.tag")),
            ],
        ),
        migrations.CreateModel(
            name="PageFollower",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user_id", models.UUIDField()),
                (
                    "page",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="page_followers",
                        to="pages.page",
                    ),
                ),
            ],
        ),
    ]
