from datetime import timedelta

from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from pages.models import Page, PageFollower
from pages.permissions import PageRolePermissions
from pages.serializers import PageFollowerSerializer, PageSerializer
from posts.models import Post
from posts.serializers import PostSerializer
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PagePagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = "limit"
    max_page_size = 100


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
            "page_posts",
        ]:
            return [PageRolePermissions()]

        return []

    def check_object_permissions(self, request, obj):
        # any logged in user can follow/unfollow and see page posts
        if self.action in ["follow", "unfollow", "page_posts"]:
            return
        # any other action requires page owner or admin/moderator
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
        page.unblock_date = timezone.now() + timedelta(minutes=15)
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

    @action(detail=True, methods=["get"])
    def page_posts(self, request, pk=None):
        page = self.get_object()
        posts = Post.objects.filter(page=page).order_by("-created_at")
        paginator = PagePagination()
        page_posts = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(page_posts, many=True)
        return paginator.get_paginated_response(serializer.data)


class FeedViewSet(viewsets.ViewSet):
    def list(self, request):
        user_id = request.user["user_id"]
        followed_pages = PageFollower.objects.filter(user_id=user_id).values_list(
            "page", flat=True
        )
        posts = Post.objects.filter(page__in=followed_pages).order_by("-created_at")
        paginator = PagePagination()
        page_posts = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(page_posts, many=True)

        return paginator.get_paginated_response(serializer.data)
