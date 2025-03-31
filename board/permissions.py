from rest_framework import permissions


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Позволяет анонимным пользователям получать список объявлений,
    а аутентифицированным пользователям — выполнять любое действие.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  # GET и HEAD запросы
            return True
        return request.user is not None and request.user.is_authenticated


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Позволяет изменения объектов только их владельцам,
    а анонимным пользователям только читать.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:  # GET и HEAD запросы
            return True
        return (
            obj.author == request.user
        )  # Проверяем, является ли пользователь владельцем
