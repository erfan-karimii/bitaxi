from rest_framework import permissions

class IsCustomer(permissions.BasePermission):
    """
    permission check for if user is valid customer or not.
    """
    message = 'You are not a valid customer!'
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.is_customer)