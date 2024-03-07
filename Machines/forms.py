from django import forms
from .models import *

class MachineAreaForm(forms.ModelForm):
    class Meta:
        model = MachineArea
        fields = ['name','area']

class MachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = ['name','machine_area']

class MachineOperatorForm(forms.ModelForm):
    class Meta:
        model = MachineOperator
        fields = '__all__'


class MachineRuntimeForm(forms.ModelForm):
    class Meta:
        model = MachineRuntime
        fields = ['start_time', 'end_time']
        exlcude = ['operator']

class MaintenanceTaskForm(forms.ModelForm):
    class Meta:
        model = MaintenanceTask
        fields = '__all__'

