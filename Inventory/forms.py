from django import forms
from .models import *
from django.forms import inlineformset_factory

class BrickProductForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Write short description'}), required=False)
    product_image = forms.ImageField(required=True)

    class Meta:
        model = BrickProduct
        fields = ['name', 'category', 'description', 'product_image']

class ProductAttributeForm(forms.ModelForm):
    class Meta:
        model = ProductAttribute
        fields = ['name','dimensions', 'price', 'stock']
        
class SalesForm(forms.ModelForm):    
    class Meta:
        model = Sale
        fields = '__all__'

class add_inventoryForm(forms.ModelForm):    
    class Meta:
        model = BrickStock
        fields = '__all__'
