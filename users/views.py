from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Payment
from .serializers import PaymentSerializer

class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['course', 'lesson', 'payment_method']  # фильтрация
    ordering_fields = ['payment_date']  # сортировка
    ordering = ['-payment_date']  # по умолчанию — от новых к старым
