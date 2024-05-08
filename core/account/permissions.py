from rest_framework import permissions


class IsAuthenticatedCustomer(permissions.BasePermission):
    """
    permission check for if user is valid customer or not.
    """

    message = "You are not a valid customer!"

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.is_customer)


class IsSuperuser(permissions.BasePermission):
    """
    permission check for if user is valid superuser or not.
    """

    message = "You are not a valid super user!"

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.is_superuser)


class IsDriver(permissions.BasePermission):
    """
    permission check for if user is valid Driver or not.
    """

    message = "You are not a valid Driver!"

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.is_driver)
