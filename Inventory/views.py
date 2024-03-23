from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db.models import Q

from .forms import BrickProductForm,SalesForm,add_inventoryForm
from .models import *
from .utils import generate_product_code

import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()


url=os.environ.get('SUPABASE_URL')
key=os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
supabase = create_client(url, key)


@login_required(login_url='login')
def inventory(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    categories = BrickCategory.objects.all()

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

            # Get the last BrickProduct ID
            last_product = BrickProduct.objects.last()
            if last_product:
                new_id = last_product.id + 1
            else:
                new_id = 1

            
            # Generate product code
            productcode = generate_product_code()

            # Create a new BrickProduct instance
            new_product = BrickProduct.objects.create(
                id=new_id,
                name=f_name,
                category=category_instance,
                description=f_description,
                dimensions=f_dimensions,
                price=f_price,
                stock=f_stock,
                product_image=f_product_image.name,
                product_code=productcode  
            )

            messages.success(request, f"New product {new_product.name} added successfully")
            
            # Upload product image to Supabase storage
            if f_product_image:
                supabase.storage.from_('image-bucket/Products').upload(f_product_image.name, f_product_image.read(), {'content-type': 'image/jpeg'})

            return redirect('add_inventory')

    else:
        formset = BrickProductForm()

    context = {
        'formset': formset,
        'categories': categories,
    }
    return render(request, 'Inventory/add_new_product.html', context)


@login_required(login_url='login')
def all_items_list(request):
    # Check if the user is a superuser
    if not request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    # Handle search query
    search_query = request.GET.get('search')
    if search_query:
        all_items_list = BrickProduct.objects.filter(
            Q(name__icontains=search_query) |
            Q(category__name__icontains=search_query)|
            Q(product_code__icontains=search_query)
        )
    else:
        all_items_list = BrickProduct.objects.all()

    form = BrickProductForm(request.POST if request.method == 'POST' else None)

    for bricks in all_items_list:
        # Get public URL for soil_img
        res = supabase.storage.from_('image-bucket/Products/').get_public_url(bricks.product_image)
        # Update soil_img field with the public URL
        bricks.product_image = res
    
    context = {
        'all_items': all_items_list,
        'forms': form
    }
    return render(request, 'Inventory/All_product_list.html', context)

@login_required(login_url='login')
def product_edit(request, pk):
    # Check if the user is a superuser
    if not request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:
        brick_product = get_object_or_404(BrickProduct, pk=pk)
        
        if request.method == 'POST':
            form = BrickProductForm(request.POST, instance=brick_product)
            if form.is_valid():
                form.save()
                return redirect('all_items_list')  # Redirect to the list view after editing
        else:
            form = BrickProductForm(instance=brick_product)
        context = {
            'forms': form,
            'brick_product': brick_product,  # Add brick_product to the context
        }
    return render(request, 'Inventory/Edit_product_Byid.html', context)


@login_required(login_url='login')
def sales_list(request):
    # Check if the user is a superuser
    if not request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:
        form =SalesForm()
        sales = Sale.objects.all()

        if request.method == 'POST':
            form = SalesForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('sales_list')  # Redirect to the list view after editing
        else:
            form = SalesForm()
        context ={
            "forms":form,
            "sales":sales,

        }
    return render(request, 'Inventory/Sales_list_add.html', context)

@login_required(login_url='login')
def add_inventory(request):
    # Check if the user is a superuser
    if not request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to access this page.")
    else:
        form =add_inventoryForm()
        add_inventory = BrickStock.objects.all()

        if request.method == 'POST':
            form = add_inventoryForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('add_inventory')  # Redirect to the list view after editing
        else:
            form = add_inventoryForm()
        context ={
            "forms":form,
            "added_inventory":add_inventory,

        }
    return render(request, 'Inventory/Add_inventory.html', context)
