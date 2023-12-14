from pages.models import Page
from posts.models import Post, PostLike
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    page = serializers.PrimaryKeyRelatedField(Page, read_only=True)

    class Meta:
        model = Post
        fields = "__all__"


class PostLikeSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)

    class Meta:
        model = PostLike
        fields = "__all__"
