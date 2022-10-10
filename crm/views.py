from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Customer, Contract, Event
from .permissions import IsInchargeOrReadOnly
from .serializers import CustomerSerializer, ContractSerializer, EventSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsInchargeOrReadOnly]
    serializer_class = CustomerSerializer

    def get_queryset(self):
        return Customer.objects.filter(
            Q(sales_contact=self.request.user) |
            Q(events__support_contact=self.request.user)
        ).distinct().select_related('sales_contact')


class ContractViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsInchargeOrReadOnly]
    serializer_class = ContractSerializer

    def get_queryset(self):
        return Contract.objects.filter(
            Q(sales_contact=self.request.user) |
            Q(customer__events__support_contact=self.request.user)
        ).distinct().select_related('sales_contact')


class EventViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsInchargeOrReadOnly]
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.filter(
            Q(support_contact=self.request.user) |
            Q(customer__sales_contact=self.request.user)
        ).distinct().select_related('support_contact', 'customer__sales_contact')
