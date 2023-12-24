from uuid import UUID

from posts.models import Post, PostLike
from posts.permissions import PostRolePermissions
from posts.serializers import PostLikeSerializer, PostSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.action in ["update", "destroy"]:
            return [PostRolePermissions()]

        return []

    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)
        for permission in self.get_permissions():
            if not permission.has_object_permission(request, self, obj):
                self.permission_denied(
                    request, message=getattr(permission, "message", None)
                )
