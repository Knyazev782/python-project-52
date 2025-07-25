from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, object):
        if not request.user.is_authenticated:
            return False
        return object.created_by == request.user