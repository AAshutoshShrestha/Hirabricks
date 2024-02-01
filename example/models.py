from django.db import models
from django.utils import timezone


STATUS_CHOICES = (
    ('INLINE', 'Inline'),
    ('COMPLETED', 'Completed'),
)

class Thermocouple(models.Model):
    name = models.CharField(max_length=50, unique=True, help_text="Name of the thermocouple")
    temperature = models.FloatField(null=True, blank=True, help_text="Temperature of the thermocouple in degrees Celsius")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['id']

class TemperatureRecord(models.Model):
    thermocouple = models.ForeignKey(Thermocouple, on_delete=models.CASCADE, related_name='temperature_records', help_text="Thermocouple associated with the temperature record")
    date = models.DateField(help_text="Date of the temperature record")
    time = models.TimeField(help_text="Time of the temperature record")
    temperature = models.FloatField(help_text="Temperature recorded in degrees Celsius")

    def __str__(self):
        return f"{self.thermocouple.name} - {self.date} {self.time} - {self.temperature}°C"

    class Meta:
        ordering = ['id']

class Zone(models.Model):
    name = models.CharField(max_length=50, help_text="Name of the zone")
    thermocouple = models.ForeignKey(Thermocouple, on_delete=models.CASCADE, related_name='zones', help_text="Thermocouple assigned to the zone")
    
    def __str__(self):
        return f"{self.name}"
     
    class Meta:
        ordering = ['id']

class Car(models.Model):
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='cars',null=True, help_text="Zone where the car is located")
    car_number = models.CharField(max_length=20, unique=True)
    entry_time = models.DateTimeField(default=timezone.now, help_text="Time when the car enters the zone")
    exit_time = models.DateTimeField(help_text="Time when the car exits the tunnel",null=True )
    status = models.CharField(max_length=20,choices=STATUS_CHOICES, default='INLINE', help_text="Status of the car (INLINE or COMPLETED)") 

    def __str__(self):
        return f"{self.car_number} - {self.status}"

     
    class Meta:
        ordering = ['id']