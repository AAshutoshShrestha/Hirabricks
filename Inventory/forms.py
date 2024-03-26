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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # If the form is being used to edit an existing instance
        if self.instance.pk:
            # Filter the queryset of product_attribute based on the product of the instance
            self.fields['product_attribute'].queryset = ProductAttribute.objects.filter(product__name=self.instance.product__name)
        else:
            # If creating a new instance, initially set an empty queryset for product_attribute
            self.fields['product_attribute'].queryset = ProductAttribute.objects.none()

    class Meta:
        model = Sale
        fields = '__all__'
        widgets = {
            'product': forms.Select(attrs={'onchange': 'update_product_attribute_choices()'}),
            'product_attribute': forms.Select(),
        }


class add_inventoryForm(forms.ModelForm):    
    class Meta:
        model = BrickStock
        fields = '__all__'
