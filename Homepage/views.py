from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ContactForm
from .models import *

from Inventory.models import BrickProduct,BrickCategory

import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()


url=os.environ.get('SUPABASE_URL')
key=os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
supabase = create_client(url, key)


def base(request):
    socialmedia = SocialLink.objects.all()
    company_info = Company_info.objects.all()
    Team_info = TeamMember.objects.all()
    context = {
        'SocialLink':socialmedia,
        'Company_info':company_info,
        'TeamMember':Team_info,
    }
    return render(request, 'Main/base.html', context)
def main(request):
    socialmedia = SocialLink.objects.all()
    company_info = Company_info.objects.all()
    Team_info = TeamMember.objects.all()
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
        'SocialLink':socialmedia,
        'Company_info':company_info,
        'TeamMember':Team_info,
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
        res = supabase.storage.from_('image-bucket/Products/').get_public_url(bricks.product_image)
        # Update product_image field with the public URL
        bricks.product_image = res
    
    context = {
        'products': products,
    }
    return render(request, 'Main/all_products.html', context)


def By_category(request, slug):
    category = get_object_or_404(BrickCategory, slug=slug)
    category_slug=category.slug

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
        res = supabase.storage.from_('image-bucket/Products/').get_public_url(bricks.product_image)
        # Update product_image field with the public URL
        bricks.product_image = res
    
    context = {
        'products': products,
        'category_empty': category_empty,
        'category': category_slug,
    }

    return render(request, 'Main/category.html', context)

def product_detail(request, slug):
    product = BrickProduct.objects.filter(slug=slug)
    for i in product:
        # Get public URL for soil_img
        res = supabase.storage.from_('image-bucket/Products/').get_public_url(i.product_image)
        # Update soil_img field with the public URL
        i.product_image = res

    context = {
        'products': product,

    }

    return render(request, 'Main/product_details.html', context)
