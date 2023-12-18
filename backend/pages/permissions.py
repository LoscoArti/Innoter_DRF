from uuid import UUID

from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user["role"] == "ADMIN"

    def has_object_permission(self, request, view, obj):
        return request.user["role"] == "ADMIN"


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user["role"] == "MODERATOR"

    def has_object_permission(self, request, view, obj):
        return (
            request.user["role"] == "MODERATOR"
            and obj.user_group_id == request.user["group_id"]
        )


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user["role"] == "USER"

    def has_object_permission(self, request, view, obj):
        return request.user["role"] == "USER" and obj.user_id == UUID(
            request.user["user_id"]
        )
