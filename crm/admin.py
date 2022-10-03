from django.contrib import admin
from .models import Customer, Contract, Event


admin.site.register(Customer)
admin.site.register(Contract)
admin.site.register(Event)
