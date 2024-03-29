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

class Dryer_EfficiencyForm(forms.ModelForm):
    class Meta:
        model = Dryer_Efficiency
        fields = ['Brick_type','Count']
        exclude = ['user','Date']


class MixtureForm(forms.ModelForm):
    type = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'What type of soil is it?'}))
    remarks = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Add notes if any'}),required=False)
    soil_img = forms.ImageField(required=False)
    soil_test_report = forms.ImageField(required=False)
    
    class Meta:
        model = SoilDetails
        fields = ['type','Source','sand','silt','clay','remarks','soil_img','soil_test_report']
        exclude = ['user','date']

# MixtureFormSet = modelformset_factory(Mixture, form=MixtureForm, extra=1)