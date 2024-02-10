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
        fields = ['car_number','remarks']
        exclude = ['user']



class TemperatureInputForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(TemperatureInputForm, self).__init__(*args, **kwargs)
        
        thermocouples = Thermocouple.objects.all()
        
        for thermocouple in thermocouples:
            field_name = f"temperature_{thermocouple.id}"
            label = f"Temperature for {thermocouple.name}"
            
            self.fields[field_name] = forms.FloatField(label=label, required=False)

    def clean(self):
        cleaned_data = super().clean()
        
        # You can add custom validation if needed
        
        return cleaned_data
