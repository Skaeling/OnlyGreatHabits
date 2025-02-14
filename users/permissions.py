from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Возвращает True, если пользователь является владельцем объекта"""

    message = 'У вас недостаточно прав доступа для данного действия.'

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
