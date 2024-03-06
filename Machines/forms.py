from django import forms
from .models import *

class MachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = ['name','area']

class MachineOperatorForm(forms.ModelForm):
    class Meta:
        model = MachineOperator
        fields = '__all__'


class MachineRuntimeForm(forms.ModelForm):
    class Meta:
        model = MachineRuntime
        fields = ['start_time', 'end_time']
        exlcude = ['operator']

