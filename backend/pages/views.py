from pages.models import Page, PageFollower
from pages.permissions import IsAdmin, IsModerator, IsUser
from pages.serializers import PageFollowerSerializer, PageSerializer
from rest_framework import generics, response, status, views


class PageCreateView(generics.ListCreateAPIView):
    queryset = Page.objects.all()
    serializer_class = PageSerializer

    def perform_create(self, serializer):
        user_info = self.request.user
        serializer.save(
            user_id=user_info["user_id"],
            user_group_id=user_info["group_id"],
            is_blocked=False,
            unblock_date=None,
        )


class PageRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Page.objects.all()
    serializer_class = PageSerializer

    def get_permissions(self):
        permissions = []
        if self.request.method == "DELETE":
            if self.request.user["role"] == "ADMIN":
                permissions.append(IsAdmin())
            elif self.request.user["role"] == "MODERATOR":
                permissions.append(IsModerator())
            elif self.request.user["role"] == "USER":
                permissions.append(IsUser())
        if self.request.method == "PATCH":
            if self.request.user["role"] == "USER":
                permissions.append(IsUser())
        return permissions

    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)
        for permission in self.get_permissions():
            if not permission.has_object_permission(request, self, obj):
                self.permission_denied(
                    request, message=getattr(permission, "message", None)
                )
