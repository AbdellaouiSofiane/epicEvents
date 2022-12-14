from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class TimeStamped(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Customer(TimeStamped):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField()
    phone = models.CharField(max_length=128)
    mobile = models.CharField(max_length=128)
    company_name = models.CharField(max_length=128)
    prospect = models.BooleanField(default=True)
    sales_contact = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"Customer: {self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Contract(TimeStamped):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    amount = models.FloatField(validators=[MinValueValidator(0.0)])
    payment_due = models.DateTimeField()
    sales_contact = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"Contract n° {self.id} of {self.amount}$"


class Event(TimeStamped):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='events')
    event_status = models.ForeignKey(Contract, on_delete=models.CASCADE)
    attendees = models.IntegerField()
    event_date = models.DateTimeField()
    notes = models.TextField()
    support_contact = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"Event scheduled for {self.event_date}"
