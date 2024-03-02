from django import forms
from .models import BurnerConsumption, JhogaiConsumption

class BurnerConsumptionForm(forms.ModelForm):
    class Meta:
        model = BurnerConsumption
        fields = ['coal_weight','burner_number']
        exclude = ['user','date']

class JhogaiConsumptionForm(forms.ModelForm):
    class Meta:
        model = JhogaiConsumption
        fields = ['type','weight']
        exclude = ['user','date']
