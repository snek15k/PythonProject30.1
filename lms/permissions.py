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


class IsOwnerOrModerator(BasePermission):
    """
    Модераторы имеют доступ ко всем объектам.
    Обычные пользователи — только к своим.
    """

    def has_object_permission(self, request, view, obj):
        is_moderator = request.user.groups.filter(name='Модераторы').exists()

        if request.method in SAFE_METHODS or request.method in ['PUT', 'PATCH', 'DELETE']:
            return is_moderator or obj.owner == request.user

        return False  # POST не разрешён, его контролирует другой
