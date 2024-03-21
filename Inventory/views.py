from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import BrickProductForm
from .models import *

import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()


url=os.environ.get('SUPABASE_URL')
key=os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
supabase = create_client(url, key)

# Create your views here.
@login_required(login_url='login')
def inventory(request):
    if request.method == 'POST':
        formset = BrickProductForm(request.POST, request.FILES)
        if formset.is_valid():
            # Extract data from the form
            f_name = request.POST.get('name')
            f_category = request.POST.get('category')
            f_description = request.POST.get('description')
            f_dimensions = request.POST.get('dimensions')
            f_price = request.POST.get('price')
            f_stock = request.POST.get('stock')
            f_product_image = request.FILES.get('product_image')

            # Retrieve the BrickCategory instance
            category_instance = BrickCategory.objects.get(pk=f_category)

            # Create a new Mixture instance
            new_product = BrickProduct.objects.create(
                name=f_name,
                category=category_instance,
                description=f_description,
                dimensions=f_dimensions,
                price=f_price,
                stock=f_stock,
                product_image= f_product_image.name,  # Save the file name in the database
            )
            # Save the Mixture instance
            new_product.save()
            
            # Upload soilimg to Supabase storage
            supabase.storage.from_('image-bucket/Products').upload(f_product_image.name, f_product_image.read(), {'content-type': 'image/jpeg'})
            return redirect('inventory')
        
    else:
        formset = BrickProductForm()
    context = {
        'formset': formset,
    }
    return render(request, 'Inventory/home.html', context)