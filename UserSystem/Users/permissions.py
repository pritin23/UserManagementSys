from rest_framework.permissions import BasePermission


class CustomUserPermission(BasePermission):
    """
        function return whether user is authenticated or not and permissions to the user according to his type
    """
    def has_permission(self, request, view):
        if request.method == 'POST' and request.user.is_authenticated:
            return False
        if request.method == 'POST':
            return False
        else:
            return True









