import os
from dotenv import load_dotenv

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import DateTimeField
from supabase import create_client, Client, ClientOptions


load_dotenv()


url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(url, key,
  options=ClientOptions(
    postgrest_client_timeout=10,
    storage_client_timeout=10
  ))

class DateTimeWithoutTZField(DateTimeField):
    def db_type(self, connection):
        return 'timestamp'
    

METHOD_CHOICES = [
    ('झोगाई Coal', 'झोगाई Coal'),
    ('झोगाई Mixed', 'झोगाई Mixed'),
    ('झोगाई WoodDust', 'झोगाई WoodDust'),
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


class SoilDetails(models.Model):
    user = models.ForeignKey(User, null=True, default='1', on_delete=models.SET_NULL)
    date = DateTimeField(help_text="Form filled date", null=True, blank=True)
    type = models.CharField(max_length=100)
    sand = models.IntegerField(default=0)
    silt = models.IntegerField(default=0)
    clay = models.IntegerField(default=0)
    remarks = models.TextField( default='No remarks',null=True, blank=True,help_text="Add remarks if any")
    soil_img = models.ImageField(upload_to ='',null=True, blank=True)

    def __str__(self):
        return f"{self.id}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.soil_img:
            with open(self.soil_img.path, 'rb') as file:
                response = supabase.storage.from_('Soils').upload(f'images/{self.soil_img.name}', file)
                if response.status_code == 201:
                    self.soil_img = response.data['Key']
                    super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.soil_img:
            response = supabase.storage.from_('Soils').remove(self.soil_img)
            if response.status_code == 200:
                self.soil_img = None
        super().delete(*args, **kwargs)

    class Meta:
        ordering = ['id']

    @classmethod
    def bulk_create_from_import(cls, data):
        cls.objects.bulk_create([cls(**item) for item in data])