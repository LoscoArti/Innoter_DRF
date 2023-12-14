from pages.models import Page
from posts.models import Post, PostLike
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    page = serializers.PrimaryKeyRelatedField(Page, read_only=True)

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
    post = PostSerializer(read_only=True)

    class Meta:
        model = PostLike
        fields = ("id", "post", "user_id")
        read_only_fields = ("id", "user_id")
