from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import PaymentListAPIView, RegisterView, UserViewSet

router = DefaultRouter()
router.register('all', UserViewSet, basename='user')  # CRUD

urlpatterns = [
    path('payments/', PaymentListAPIView.as_view(), name='payment-list'),
    path('register/', RegisterView.as_view(), name='register'),  # регистрация
]

urlpatterns += router.urls
