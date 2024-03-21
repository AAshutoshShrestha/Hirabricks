from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone

from .forms import ContactForm
from .models import *

from Inventory.models import BrickProduct

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

def products(request):
    all_bricks = BrickProduct.objects.all()
    for bricks in all_bricks:
        # Get public URL for soil_img
        res = supabase.storage.from_('image-bucket/Products/').get_public_url(bricks.product_image)
        # Update soil_img field with the public URL
        bricks.product_image = res
    context = {
        'products':all_bricks,
    }
    return render(request, 'Main/all_products.html', context)

def product_detail(request, product_id):
    product = BrickProduct.objects.filter(id=product_id)
    for i in product:
        # Get public URL for soil_img
        res = supabase.storage.from_('image-bucket/Products/').get_public_url(i.product_image)
        # Update soil_img field with the public URL
        i.product_image = res

    context = {
        'products': product
    }

    return render(request, 'Main/product_details.html', context)

