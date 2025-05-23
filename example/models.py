# Import necessary modules
from django.db import models
from django.contrib.auth.models import User
from django.db.models import DateTimeField

# Import related model
from conditions.models import MultiCondition

# Choices for status
STATUS_CHOICES = (
    ('INLINE', 'Inline'),
    ('COMPLETED', 'Completed'),
)

# Choices for section
SECTION_CHOICES = (
    ('PRE HEATING', 'Pre Heating'),
    ('HEATING', 'Heating'),
    ('COOLING', 'Cooling'),
)

# Custom DateTimeField without time zone
class DateTimeWithoutTZField(DateTimeField):
    def db_type(self, connection):
        return 'timestamp'
    
# Model for Thermocouple
class Thermocouple(models.Model):
    name = models.CharField(max_length=50, unique=True, help_text="Name of the thermocouple")
    
    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['id']

    # Method to bulk create Thermocouple objects from import data
    @classmethod
    def bulk_create_from_import(cls, data):
        cls.objects.bulk_create([cls(**item) for item in data])

# Model for TemperatureRecord
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

    # Method to bulk create TemperatureRecord objects from import data
    @classmethod
    def bulk_create_from_import(cls, data):
        cls.objects.bulk_create([cls(**item) for item in data])

# Function to create dynamically temperature fields for each thermocouple
def create_temperature_field(name):
    return models.IntegerField(null=True, blank=True, verbose_name=name)

# Dynamically create fields for each thermocouple
thermocouples = Thermocouple.objects.all()
for thermocouple in thermocouples:
    field_name = thermocouple.name.lower().replace(" ", "_")
    TemperatureRecord.add_to_class(field_name, create_temperature_field(thermocouple.name))

# Model for Zone
class Zone(models.Model):
    name = models.CharField(max_length=50, help_text="Name of the zone")
    thermocouple = models.ForeignKey(Thermocouple, on_delete=models.CASCADE, related_name='zones', help_text="Thermocouple assigned to the zone")
    area = models.CharField(max_length=20, choices=SECTION_CHOICES, default='Pre Heating', help_text="SECTION ZONES CATEGORY")
    
    def __str__(self):
        return f"{self.name}"
     
    class Meta:
        ordering = ['id']
    
    # Method to bulk create Zone objects from import data
    @classmethod
    def bulk_create_from_import(cls, data):
        cls.objects.bulk_create([cls(**item) for item in data])

# Model for Car
class Car(models.Model):
    user = models.ForeignKey(User, null=True, default='1', on_delete=models.SET_NULL)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='cars', null=True, help_text="Zone where the car is located")
    car_number = models.CharField(max_length=20)
    entry_time = DateTimeField(help_text="Time when the car enters the zone", null=True, blank=True)
    exit_time = DateTimeField(help_text="Time when the car exits the tunnel", null=True, blank=True)
    Type = models.ForeignKey(MultiCondition, null=True, default='1', on_delete=models.SET_NULL, help_text="Type of product stacked in the car")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='INLINE', help_text="Status of the car (INLINE or COMPLETED)") 
    remarks = models.TextField(default='No remarks', null=True, blank=True)

    def __str__(self):
        return f"{self.car_number} - {self.status}"

    class Meta:
        ordering = ['zone']

    # Method to bulk create Car objects from import data
    @classmethod
    def bulk_create_from_import(cls, data):
        cls.objects.bulk_create([cls(**item) for item in data])

# Model for Firing
class Firing(models.Model):
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='Firing',null=True, help_text="Zone where the Firing is located")
    
    def __str__(self):
        return f"{self.zone}"

    class Meta:
        ordering = ['id']

    # Method to bulk create Firing objects from import data
    @classmethod
    def bulk_create_from_import(cls, data):
        cls.objects.bulk_create([cls(**item) for item in data])
