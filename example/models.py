from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User 
from django.db.models import DateTimeField

from conditions.models import MultiCondition

STATUS_CHOICES = (
    ('INLINE', 'Inline'),
    ('COMPLETED', 'Completed'),
)

Section_choise =(
    ('PRE HEATING','Pre Heating'),
    ('HEATING','Heating'),
    ('COOLING','Cooling'),
)

class DateTimeWithoutTZField(DateTimeField):
    def db_type(self, connection):
        return 'timestamp'
    

class Thermocouple(models.Model):
    name = models.CharField(max_length=50, unique=True, help_text="Name of the thermocouple")
    
    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['id']

    @classmethod
    def bulk_create_from_import(cls, data):
        cls.objects.bulk_create([cls(**item) for item in data])








class TemperatureRecord(models.Model):
    user = models.ForeignKey(User, null=True, default='1', on_delete=models.SET_NULL)
    date = models.DateField(help_text="Date of the temperature record")
    time = models.TimeField(help_text="Time of the temperature record")

    class Meta:
        verbose_name = "Temperature Record"
        verbose_name_plural = "Temperature Records"
        ordering = ['id']

    def __str__(self):
        return f"{self.thermocouple.name} - {self.date} {self.time} - {self.temperature}°C"


    @classmethod
    def bulk_create_from_import(cls, data):
        cls.objects.bulk_create([cls(**item) for item in data])

def create_temperature_field(name):
    return models.IntegerField(null=True, blank=True, verbose_name=name)

# Dynamically create fields for each thermocouple
thermocouples = Thermocouple.objects.all()
for thermocouple in thermocouples:
    field_name = thermocouple.name.lower().replace(" ", "_")
    TemperatureRecord.add_to_class(field_name, create_temperature_field(thermocouple.name))








class Zone(models.Model):
    name = models.CharField(max_length=50, help_text="Name of the zone")
    thermocouple = models.ForeignKey(Thermocouple, on_delete=models.CASCADE, related_name='zones', help_text="Thermocouple assigned to the zone")
    area = models.CharField(max_length=20,choices=Section_choise, default='Pre Heating', help_text="SECTION ZONES CATEGORY")
    
    def __str__(self):
        return f"{self.name}"
     
    class Meta:
        ordering = ['id']
    
    @classmethod
    def bulk_create_from_import(cls, data):
        cls.objects.bulk_create([cls(**item) for item in data])








class Car(models.Model):
    user = models.ForeignKey(User, null=True, default='1', on_delete=models.SET_NULL)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='cars', null=True, help_text="Zone where the car is located")
    car_number = models.CharField(max_length=20)
    entry_time = DateTimeField(help_text="Time when the car enters the zone", null=True, blank=True)
    exit_time = DateTimeField(help_text="Time when the car exits the tunnel", null=True, blank=True)
    Type = models.ForeignKey(MultiCondition, null=True, default='1', on_delete=models.SET_NULL, help_text="Type of product stacked in the car")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='INLINE', help_text="Status of the car (INLINE or COMPLETED)") 
    remarks = models.TextField( default='No remarks',null=True, blank=True)

    def __str__(self):
        return f"{self.car_number} - {self.status}"

    class Meta:
        ordering = ['zone']

    @classmethod
    def bulk_create_from_import(cls, data):
        cls.objects.bulk_create([cls(**item) for item in data])








class Firing(models.Model):
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='Firing',null=True, help_text="Zone where the Firing is located")
    
    def __str__(self):
        return f"{self.zone}"

     
    class Meta:
        ordering = ['id']

    @classmethod
    def bulk_create_from_import(cls, data):
        cls.objects.bulk_create([cls(**item) for item in data])