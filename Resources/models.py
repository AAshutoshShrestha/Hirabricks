import os
from dotenv import load_dotenv
from django.utils.html import mark_safe
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import DateTimeField
from supabase import create_client, Client, ClientOptions

from django.utils.html import format_html

load_dotenv()


url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(url, key)

class DateTimeWithoutTZField(DateTimeField):
    def db_type(self, connection):
        return 'timestamp'
    

METHOD_CHOICES = [
    ('झोगाई Coal', 'झोगाई Coal'),
    ('झोगाई Mixed', 'झोगाई Mixed'),
    ('झोगाई WoodDust', 'झोगाई WoodDust'),
]

brick_type = [
    ('दचि', 'दचि'),
    ('सानो बुता', 'सानो बुता'),
    ('ठूलो बुता', 'ठूलो बुता'),
]
Soilsource_CHOICES = [
    ('Gokarna', 'Gokarna'),
    ('Chyasal', 'Chyasal'),
    ('Min Bhawan', 'Min Bhawan'),
    ('Satungal', 'Satungal'),
    ('Kharipati', 'Kharipati'),
    ('Tuwachwok', 'Tuwachwok'),
    ('Gundu', 'Gundu'),
    ('Other', 'Other'),
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
    soil_test_report = models.ImageField(upload_to ='Reports',null=True, blank=True)
    Source = models.CharField(max_length=20, choices=Soilsource_CHOICES)
    
    def soil_img_display(self):
        res = supabase.storage.from_('image-bucket').get_public_url(self.soil_img)
        return format_html('<img src="{}" width="100" height="100">', res)
    
    def soil_test_report_display(self):
        res = supabase.storage.from_('image-bucket/Reports').get_public_url(self.soil_test_report)
        return format_html('<img src="{}" width="100" height="100">', res)
    
    def export_soil_img(self):
        res = supabase.storage.from_('image-bucket').get_public_url(self.soil_img)
        return (res)
    
    def export_Soil_testrep(self):
        res = supabase.storage.from_('image-bucket/Reports').get_public_url(self.soil_test_report)
        return (res)
        

    def __str__(self):
        return f"{self.id}"
    
    class Meta:
        ordering = ['id']

    @classmethod
    def bulk_create_from_import(cls, data):
        cls.objects.bulk_create([cls(**item) for item in data])


class Dryer_Efficiency(models.Model):
    user = models.ForeignKey(User, null=True, default='1', on_delete=models.SET_NULL)
    Date = models.DateTimeField(null=True, blank=True)
    Brick_type = models.CharField(max_length=20, choices=brick_type)
    Count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.id}"
    
    class Meta:
        ordering = ['id']

    @classmethod
    def bulk_create_from_import(cls, data):
        cls.objects.bulk_create([cls(**item) for item in data])