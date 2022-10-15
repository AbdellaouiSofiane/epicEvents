from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ValidationError

from .filters import ContractFilter, EventFilter
from .models import Customer, Contract, Event
from .permissions import IsInchargeOrReadOnly
from .serializers import CustomerSerializer, ContractSerializer, EventSerializer


class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsInchargeOrReadOnly]
    http_method_names = ['get', 'post', 'put', 'patch', 'head', 'options', 'trace'] # No Delete

    def perform_create(self, serializer):
        if not self.request.user.groups.filter(
            name='sales employees'
        ).exists():
            raise ValidationError(
                'You are not permitted to create a customer'
            )
        super().perform_create(serializer)


class CustomerViewSet(BaseViewSet):
    serializer_class = CustomerSerializer
    filterset_fields = ('last_name', 'email')

    def get_queryset(self):
        return Customer.objects.filter(
            Q(sales_contact=self.request.user) |
            Q(events__support_contact=self.request.user)
        ).distinct().select_related('sales_contact')


class ContractViewSet(BaseViewSet):
    serializer_class = ContractSerializer
    filterset_class = ContractFilter

    def get_queryset(self):
        return Contract.objects.filter(
            Q(sales_contact=self.request.user) |
            Q(customer__events__support_contact=self.request.user)
        ).distinct().select_related('sales_contact')


class EventViewSet(BaseViewSet):
    serializer_class = EventSerializer
    filterset_class = EventFilter

    def get_queryset(self):
        return Event.objects.filter(
            Q(support_contact=self.request.user) |
            Q(customer__sales_contact=self.request.user)
        ).distinct().select_related('support_contact', 'customer__sales_contact')
