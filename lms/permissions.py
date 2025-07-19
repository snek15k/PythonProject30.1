from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsModeratorOrReadOnlyEdit(BasePermission):
    """
    Позволяет просматривать и редактировать, если пользователь — модератор.
    Запрещает создание и удаление.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated  # чтение — всем авторизованным
        elif request.method in ['PUT', 'PATCH']:
            return request.user.groups.filter(name='Модераторы').exists() or request.user.is_superuser
        return False  # POST, DELETE — запрещены

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsOwner(BasePermission):
    """
    Доступ только владельцу объекта.
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
