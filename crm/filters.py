from django_filters import rest_framework as filters

from .models import Contract, Event


class ContractFilter(filters.FilterSet):
    last_name = filters.CharFilter(
        field_name="customer__last_name", lookup_expr='iexact')
    email = filters.CharFilter(
        field_name="customer__email", lookup_expr='iexact')

    class Meta:
        model = Contract
        fields = ['last_name', 'email', 'payment_due', 'amount']


class EventFilter(filters.FilterSet):
    last_name = filters.CharFilter(
        field_name="customer__last_name", lookup_expr='iexact')
    email = filters.CharFilter(
        field_name="customer__email", lookup_expr='iexact')

    class Meta:
        model = Event
        fields = ['last_name', 'email', 'event_date']
