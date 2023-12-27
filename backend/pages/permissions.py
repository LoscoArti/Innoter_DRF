from rest_framework import permissions
from utils.custom_permissions import IsAdmin, IsModerator, IsUser


class PageRolePermissions(permissions.BasePermission):
    role_permissions = {
        "ADMIN": IsAdmin(),
        "MODERATOR": IsModerator(),
        "USER": IsUser(),
    }

    def has_permission(self, request, view):
        current_role = self.role_permissions.get(request.user["role"], IsUser())
        return current_role.has_permission(request=request, view=view)

    def has_object_permission(self, request, view, obj):
        current_role = self.role_permissions.get(request.user["role"], IsUser())
        return current_role.has_object_permission(request=request, view=view, obj=obj)
