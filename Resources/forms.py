from django import forms
from .models import *

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


class MixtureForm(forms.ModelForm):
    type = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'What type of soil is it?'}))
    remarks = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Add notes if any'}),required=False)
    soil_img = forms.ImageField(required=False)
    
    class Meta:
        model = SoilDetails
        fields = ['type','sand','silt','clay','remarks','soil_img']
        exclude = ['user','date']

# MixtureFormSet = modelformset_factory(Mixture, form=MixtureForm, extra=1)