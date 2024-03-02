from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class DateTimeWithoutTZField(models.DateTimeField):
    def db_type(self, connection):
        return 'timestamp'


METHOD_CHOICES = [
    ('Coal Only', 'Coal Only'),
    ('Mixed', 'Mixed'),
    ('Wood Dust', 'Wood Dust'),
]


class BurnerConsumption(models.Model):
    user = models.ForeignKey(User, null=True, default=1, on_delete=models.SET_NULL)
    date = models.DateTimeField(help_text="Time when the Coal was USED", null=True, blank=True)
    coal_weight = models.DecimalField(max_digits=10, decimal_places=2)
    burner_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.burner_number}"

    class Meta:
        ordering = ['id']

    @classmethod
    def bulk_create_from_import(cls, data):
        cls.objects.bulk_create([cls(**item) for item in data])


class JhogaiConsumption(models.Model):
    user = models.ForeignKey(User, null=True, default=1, on_delete=models.SET_NULL)
    date = models.DateTimeField(help_text="Time when the Coal was USED", null=True, blank=True)
    type = models.CharField(max_length=20, choices=METHOD_CHOICES)
    weight = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.type}"

    class Meta:
        ordering = ['id']

    @classmethod
    def bulk_create_from_import(cls, data):
        cls.objects.bulk_create([cls(**item) for item in data])
