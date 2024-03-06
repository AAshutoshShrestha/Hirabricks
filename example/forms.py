from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.utils import timezone

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

class TemperatureRecordForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(TemperatureRecordForm, self).__init__(*args, **kwargs)
        thermocouples = Thermocouple.objects.all()
        for thermocouple in thermocouples:
            field_name = thermocouple.name.lower().replace(" ", "_")
            self.fields[field_name] = forms.IntegerField(required=False)

    class Meta:
        model = TemperatureRecord
        fields = ['date', 'time', 'user']
