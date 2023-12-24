from pages.models import Page, PageFollower
from pages.permissions import PageRolePermissions
from pages.serializers import PageFollowerSerializer, PageSerializer
from posts.serializers import PostSerializer
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class PageViewSet(viewsets.ModelViewSet):
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

    def get_permissions(self):
        if self.action in [
            "create",
            "list",
            "my_pages",
            "follow",
            "unfollow",
            "followers",
            "update",
            "partial_update",
            "destroy",
            "block",
            "post",
        ]:
            return [PageRolePermissions()]

        return []

    def check_object_permissions(self, request, obj):
        if self.action in ["follow", "unfollow"]:
            return
        super().check_object_permissions(request, obj)
        for permission in self.get_permissions():
            if not permission.has_object_permission(request, self, obj):
                self.permission_denied(
                    request, message=getattr(permission, "message", None)
                )

    @action(detail=False, methods=["get"])
    def my_pages(self, request):
        pages = Page.objects.filter(user_id=request.user["user_id"])
        serializer = self.get_serializer(pages, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["patch"])
    def follow(self, request, pk=None):
        page = self.get_object()
        page_follower, created = PageFollower.objects.get_or_create(
            user_id=request.user["user_id"], page=page
        )
        if not created:
            return Response(
                {"detail": "You are already following this page."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["patch"])
    def unfollow(self, request, pk=None):
        page = self.get_object()
        try:
            page_follower = PageFollower.objects.get(
                user_id=request.user["user_id"], page=page
            )
            page_follower.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PageFollower.DoesNotExist:
            return Response(
                {"detail": "You are not following this page."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True, methods=["get"])
    def followers(self, request, pk=None):
        page = self.get_object()
        followers = PageFollower.objects.filter(page=page)
        serializer = PageFollowerSerializer(followers, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["patch"])
    def block(self, request, pk=None):
        page = self.get_object()

        for permission in self.get_permissions():
            if not permission.has_object_permission(request, self, page):
                self.permission_denied(
                    request, message=getattr(permission, "message", None)
                )

        page.is_blocked = True
        page.save()

        return Response({"detail": "Page has been blocked."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def post(self, request, pk=None):
        page = self.get_object()
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(page=page)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
