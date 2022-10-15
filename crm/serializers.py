from rest_framework import serializers
from .models import Customer, Contract, Event


class CustomerSerializer(serializers.ModelSerializer):
    sales_contact = serializers.CharField(
        source='sales_contact.username', read_only=True)

    class Meta:
        model = Customer
        fields = ('__all__')


class ContractSerializer(serializers.ModelSerializer):
    sales_contact = serializers.CharField(
        source='sales_contact.username', read_only=True)

    class Meta:
        model = Contract
        fields = ('__all__')


class EventSerializer(serializers.ModelSerializer):
    support_contact = serializers.CharField(
        source='support_contact.username', read_only=True)

    class Meta:
        model = Event
        fields = ('__all__')
