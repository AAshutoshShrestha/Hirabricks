from django.db import models

class condition(models.Model):
    name = models.CharField(max_length=50, unique=True, help_text="Name of the thermocouple")
    Fan_Speed = models.FloatField(null=True, blank=True, help_text="Speed for Fan")
    Dryer_Speed = models.FloatField(null=True, blank=True, help_text="Speed for Dryer")
    Burner_Speed = models.FloatField(null=True, blank=True, help_text="Speed for Burner")
    Temperature = models.IntegerField(null=True, blank=True, help_text="Temperature")
    Durations = models.IntegerField(null=True, blank=True, help_text="Duration to keep car in main firing zone ")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['id']