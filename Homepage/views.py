from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ContactForm
from .models import *
import requests
from django.http import JsonResponse
from Inventory.models import BrickProduct,BrickCategory,ProductAttribute    

import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()


url=os.environ.get('SUPABASE_URL')
key=os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
supabase = create_client(url, key)

def main(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            homepage_C_name = request.POST.get('name')
            homepage_C_email = request.POST.get('email')
            homepage_C_message = request.POST.get('message')
            Bform = ContactMessage.objects.create(
                name=homepage_C_name,
                email=homepage_C_email,
                message=homepage_C_message,
                created_at=timezone.now(),
            )
            Bform.save()
            messages.success(request, 'Your message has been sent successfully!')  # Sending success message
    else:
        form = ContactForm()
    context = {
        'form':form,
    }
    return render(request, 'Main/home.html', context)


def all_products(request):
    all_bricks = BrickProduct.objects.all()
    
    paginator = Paginator(all_bricks, 12)  # 12 products per page
    page_number = request.GET.get('page')
    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)
    
    for bricks in products:
        # Get public URL for product_image
        res = supabase.storage.from_('Products_image').get_public_url(bricks.product_image)
        # Update product_image field with the public URL
        bricks.product_image = res
    
    context = {
        'products': products,
    }
    return render(request, 'Main/all_products.html', context)


def By_category(request, slug):
    category = get_object_or_404(BrickCategory, slug=slug)
    category_name=category

    product_by_category = BrickProduct.objects.filter(category=category).order_by('id')
    paginator = Paginator(product_by_category, 12)  # 12 products per page
    category_empty = not product_by_category.exists()


    page_number = request.GET.get('page')
    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)
    
    for bricks in products:
        # Get public URL for product_image
        res = supabase.storage.from_('Products_image').get_public_url(bricks.product_image)
        # Update product_image field with the public URL
        bricks.product_image = res
    
    context = {
        'products': products,
        'category_empty': category_empty,
        'category': category_name,
    }

    return render(request, 'Main/category.html', context)

def product_detail(request, slug):
    product = BrickProduct.objects.get(slug=slug)
    product_attributes = product.productattribute_set.all().values('name','dimensions','price','stock')

    
    # Convert Decimal objects to float
    product_attributes_json = []
    for attribute in product_attributes:
        product_attributes_json.append({
            'name': attribute['name'],
            'dimensions': attribute['dimensions'],
            'price': float(attribute['price']),
            'stock': attribute['stock'],
        })

    # Get public URL for product image
    res = supabase.storage.from_('Products_image').get_public_url(product.product_image)
    # Update product image field with the public URL
    product.product_image = res

    context = {
        'products': product,
        'product_attributes_json': product_attributes_json,  # Convert to JSON

    }

    return render(request, 'Main/product_details.html', context)


def gallery(request):
    object_names = supabase.storage.from_('Products_image').list()
    all_names = [name['name'] for name in object_names]

    # Generate individual public URLs for each image
    individual_public_urls = [
        f"https://govmngfhcfddnuqorust.supabase.co/storage/v1/object/public/Products_image/{name}"
        for name in all_names
    ]
    context ={
        'images': individual_public_urls ,
    }
    return render(request, 'Main/gallery.html', context)
