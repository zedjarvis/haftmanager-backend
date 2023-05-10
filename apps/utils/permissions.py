from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):
    """
    Object-level permission to only allow onwner to view or edit objects.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsOwnerOrAdmin(BasePermission):
    """
    Object-level permission to only allow owners or admins to view and edit objects.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        return obj.user == request.user


class IsCreatedBy(BasePermission):
    """
    Object-level permission to only allow users to view or edit items they created.
    """

    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user


class IsCreatedByOrAdmin(BasePermission):
    """
    Object-level permission to allow users and or admins to view or edit items they created.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        return obj.created_by == request.user
