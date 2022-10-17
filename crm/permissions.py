from django.db.models import Q
from rest_framework import permissions

from .models import Customer, Contract, Event


class IsInchargeOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(
            Q(name='support employees') | Q(name='sales employees')
        ).exists()

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.groups.filter(name='support employees').exists():
            if isinstance(obj, Event):
                return obj.support_contact == request.user

        if request.user.groups.filter(name='sales employees').exists():
            if isinstance(obj, Customer) or isinstance(obj, Contract):
                return obj.sales_contact == request.user
            if isinstance(obj, Event):
                return obj.customer.sales_contact == request.user

        return False
