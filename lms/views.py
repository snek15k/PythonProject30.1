from rest_framework import viewsets
from .models import Course
from .serializers import CourseSerializer
from rest_framework import generics
from .models import Lesson
from .serializers import LessonSerializer
from .permissions import IsModeratorOrReadOnlyEdit, IsOwnerOrModerator
from users.permissions import IsModerator, IsOwnerOrModerator
from rest_framework.permissions import IsAuthenticated

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwnerOrModerator]
        elif self.action in ['create', 'destroy']:
            # Только владельцы, не модераторы
            self.permission_classes = [IsAuthenticated, IsOwnerOrModerator]
        return [permission() for permission in self.permission_classes]


    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Модераторы').exists():
            return Course.objects.all()
        return Course.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Модераторы').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.request.method == 'POST':
            # Только владельцы, не модераторы
            self.permission_classes = [IsAuthenticated, IsOwnerOrModerator]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwnerOrModerator]
        elif self.request.method == 'DELETE':
            self.permission_classes = [IsAuthenticated, IsOwnerOrModerator]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]
