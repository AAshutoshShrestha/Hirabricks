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
        fields = ['start_time', 'end_time','not_working','reason']
        exlcude = ['operator']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance and instance.not_working:
            self.fields['reason'].widget.attrs['style'] = ''  # Show the reason field
        else:
            self.fields['reason'].widget.attrs['style'] = 'display:none'

class MaintenanceTaskForm(forms.ModelForm):
    class Meta:
        model = MaintenanceTask
        fields = ['area','machine','title','description']
        exlcude = ['status','date','remarks']

class MaintenanceUpdateForm(forms.ModelForm):
    class Meta:
        model = MaintenanceTask
        fields = ['area','machine','title','description','status','remarks']
        exlcude = ['date']

