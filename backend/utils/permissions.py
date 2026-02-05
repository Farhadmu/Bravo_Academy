from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    The request is authenticated as a user, but only staff/admin users can write/edit/delete.
    Read-only for everyone else.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
