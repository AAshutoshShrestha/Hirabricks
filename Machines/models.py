from django.db import models
from django.contrib.auth.models import User

class MachineArea(models.Model):
    name = models.CharField(max_length=50, help_text="Name for the machine")
    area = models.CharField(max_length=50, help_text="Machine place")
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
    
    @classmethod
    def bulk_create_from_import(cls, data):
        cls.objects.bulk_create([cls(**item) for item in data])

class Machine(models.Model):
    machine_area = models.ForeignKey(MachineArea, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=50, help_text="Name for the machine")
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
    
    @classmethod
    def bulk_create_from_import(cls, data):
        cls.objects.bulk_create([cls(**item) for item in data])
        
STATUS_CHOICES = (
    ('Pending', 'Pending'), 
    ('Onprocess', 'On Process'), 
    ('Completed', 'Completed'),
)


class MaintenanceTask(models.Model):
    Area = models.ForeignKey(MachineArea, on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    position = models.IntegerField(default=0)


class MachineOperator(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=50, help_text="Name for the machine operator")
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='operators')

    def __str__(self):
        return self.name
     
    class Meta:
        ordering = ['id']
    
    @classmethod
    def bulk_create_from_import(cls, data):
        cls.objects.bulk_create([cls(**item) for item in data])

class MachineRuntime(models.Model):
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    machine_operator = models.ForeignKey(MachineOperator, on_delete=models.CASCADE, related_name='runtime_entries')

    def __str__(self):
        return f"MachineRuntime ID: {self.pk}"  

    def Machine_name(self):
        return self.machine_operator.machine.name
    
    def Worked_hours(self):
        if self.start_time and self.end_time:
            duration = self.end_time - self.start_time
            hours, remainder = divmod(duration.total_seconds(), 3600)
            minutes, _ = divmod(remainder, 60)
            if hours == 0:
                if minutes == 1:
                    return "{} minute".format(int(minutes))
                else:
                    return "{} minutes".format(int(minutes))
            elif minutes == 0:
                if hours == 1:
                    return "{} hour".format(int(hours))
                else:
                    return "{} hours".format(int(hours))
            else:
                return "{} hours & {} minutes".format(int(hours), int(minutes))
        else:
            return f"Running State"
        
    class Meta:
        ordering = ['id']
    
    @classmethod
    def bulk_create_from_import(cls, data):
        cls.objects.bulk_create([cls(**item) for item in data])
