from django.db import models

class MultiCondition(models.Model):
    name = models.CharField(max_length=50, unique=True, help_text="Name of the thermocouple")
    fan_speed = models.FloatField(null=True, blank=True, help_text="Speed for Fan")
    dryer_speed = models.FloatField(null=True, blank=True, help_text="Speed for Dryer")
    burner_speed = models.FloatField(null=True, blank=True, help_text="Speed for Burner")
    temperature = models.IntegerField(null=True, blank=True, help_text="Temperature")
    durations = models.IntegerField(null=True, blank=True, help_text="Duration to keep car in main firing zone")
    capacity = models.IntegerField(null=True, blank=True, help_text="No. of bricks in a car")
    is_multi_type = models.BooleanField(default=False, help_text="Check if it's a multi-type condition")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['id']


class MultiItem(models.Model):
    multi_condition = models.ForeignKey(MultiCondition, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    capacity = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.capacity})"
