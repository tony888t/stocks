from rest_framework import permissions


class isAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and request.user.groups.filter(name="Admin").exists()
        )


class IsInvestorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.groups.filter(name="Investors").exists()
        )
