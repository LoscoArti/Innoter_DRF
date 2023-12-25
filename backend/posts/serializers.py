from pages.models import Page
from pages.serializers import PageSerializer
from posts.models import Post, PostLike
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    page = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "page",
            "content",
            "reply_to",
            "likes_user_ids",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ("id", "post", "user_id", "created_at")
        read_only_fields = ("id", "created_at")
