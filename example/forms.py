from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import *

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User		
		fields = ['username', 'email', 'password1', 'password2']

class CarEntryForm(forms.ModelForm):
    car_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter latest Car Number'}))
    remarks = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Add notes if any'}),required=False)
    
    class Meta:
        model = Car
        fields = ['car_number','Type','remarks']
        exclude = ['user']

class TemperatureRecordForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TemperatureRecordForm, self).__init__(*args, **kwargs)
        thermocouples = Thermocouple.objects.all()
        for thermocouple in thermocouples:
            field_name = thermocouple.name.lower().replace(" ", "_")
            self.fields[field_name] = forms.IntegerField(required=False)

    class Meta:
        model = TemperatureRecord   
        fields = ['thermocouples_1', 'thermocouples_2', 'thermocouples_3', 'thermocouples_4', 'thermocouples_5', 'thermocouples_6', 'thermocouples_7', 'thermocouples_8', 'thermocouples_9', 'thermocouples_10', 'thermocouples_11', 'thermocouples_12']
