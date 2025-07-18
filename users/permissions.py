from rest_framework.permissions import BasePermission

class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='Модераторы').exists()

class IsOwnerOrModerator(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='Модераторы').exists():
            return True
        return obj.owner == request.user
