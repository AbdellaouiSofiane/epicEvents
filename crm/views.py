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
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filterset_fields = ('last_name', 'email')


class ContractViewSet(BaseViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    filterset_class = ContractFilter



class EventViewSet(BaseViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filterset_class = EventFilter
