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

    def perform_create(self, serializer, **kwargs):
        if not self.request.user.groups.filter(
            name='sales employees'
        ).exists():
            raise ValidationError(
                f'You are not permitted to create a {serializer.Meta.model.__name__}'
            )
        serializer.save(**kwargs)


class CustomerViewSet(BaseViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filterset_fields = ('last_name', 'email')

    def perform_create(self, serializer):
        super().perform_create(serializer, sales_contact=self.request.user)


class ContractViewSet(BaseViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    filterset_class = ContractFilter

    def perform_create(self, serializer):
        related_customer = serializer.validated_data.get('customer')
        if related_customer.prospect:
            raise ValidationError(
                'Prospects are not allowed to have contracts'
            )
        super().perform_create(serializer, sales_contact=self.request.user)


class EventViewSet(BaseViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filterset_class = EventFilter

    def perform_create(self, serializer):
        related_contract = serializer.validated_data.get('event_status')
        if not related_contract.status:
            raise ValidationError(
                'You are not permitted to create an event for an unsigned contract'
            )
        super().perform_create(serializer)
