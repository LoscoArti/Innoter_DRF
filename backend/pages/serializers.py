from pages.models import Page, PageFollower
from rest_framework import serializers


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = (
            "id",
            "name",
            "description",
            "user_id",
            "user_group_id",
            "image_url",
            "tags",
            "is_blocked",
            "unblock_date",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "user_id",
            "user_group_id",
            "created_at",
            "updated_at",
        )


class PageFollowerSerializer(serializers.ModelSerializer):
    page = PageSerializer(read_only=True)

    class Meta:
        model = PageFollower
        fields = ("id", "page", "user_id")
        read_only_fields = ("id",)
