from rest_framework import permissions


class IsLoggedIn(permissions.BasePermission):
    def has_permission(self, request, view):
        return "user_id" in request.user
