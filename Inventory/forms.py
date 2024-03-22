from django import forms
from .models import *

class BrickProductForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Write short description'}),required=False)
    dimensions = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Provide dimensions of Brick'}),required=False)
    product_image = forms.ImageField(required=True)
    
    class Meta:
        model = BrickProduct
        fields = ['name','category','description','dimensions','price','stock','product_image',]

class SalesForm(forms.ModelForm):    
    class Meta:
        model = Sale
        fields = '__all__'
