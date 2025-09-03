from rest_framework import permissions


class IsAuthorOwner(permissions.BasePermission):
    """
    Allow access only to authors owned by the logged-in user.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.user_id == request.user.id
