from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone

from django.forms import inlineformset_factory
from .forms import *
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

    # Import ProductAttributeFormSet here
    ProductAttributeFormSet = inlineformset_factory(BrickProduct, ProductAttribute, form=ProductAttributeForm, extra=1)

    if request.method == 'POST':
        form = BrickProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_product = form.save(commit=False)
            new_product.product_image = new_product.product_image.name
            new_product.product_code = generate_product_code()
            new_product.save()

            # Upload product image to Supabase storage
            supabase.storage.from_('image-bucket/').upload(new_product.product_image.name, new_product.product_image.read(), {'content-type': 'image/jpeg'})

            # Process product attributes formset
            product_attribute_formset = ProductAttributeFormSet(request.POST, instance=new_product)
            if product_attribute_formset.is_valid():
                product_attribute_formset.save()

                messages.success(request, f"New product {new_product.name} added successfully")
                return redirect('inventory')
        else:
            product_attribute_formset = ProductAttributeFormSet(request.POST)

    else:
        form = BrickProductForm()
        product_attribute_formset = ProductAttributeFormSet()

    context = {
        'form': form,
        'product_attribute_formset': product_attribute_formset,
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
            Q(category__name__icontains=search_query) |
            Q(product_code__icontains=search_query)
        )
    else:
        all_items_list = BrickProduct.objects.all()

    # Convert Decimal objects to float
    product_attributes_json = []
    for brick_product in all_items_list:
        attributes = brick_product.productattribute_set.all().values('name', 'dimensions', 'price', 'stock')
        for attribute in attributes:
            product_attributes_json.append({
                'name': attribute['name'],
                'dimensions': attribute['dimensions'],
                'price': float(attribute['price']),
                'stock': attribute['stock'],
            })

    # Handle Pagination
    paginator = Paginator(all_items_list, 12)  # 12 products per page
    page_number = request.GET.get('page')
    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)

    form = BrickProductForm(request.POST if request.method == 'POST' else None)

    for brick_product in products:
        # Get public URL for product_image
        res = supabase.storage.from_('image-bucket/Products/').get_public_url(brick_product.product_image)
        # Update product_image field with the public URL
        brick_product.product_image = res

    context = {
        'all_items': products,
        'product_attributes_json': product_attributes_json,  # Convert to JSON
        'forms': form
    }
    return render(request, 'Inventory/All_product_list.html', context)


@login_required(login_url='login')
def product_edit(request, pk):
    # Check if the user is a superuser
    if not request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to access this page.")

    brick_product = get_object_or_404(BrickProduct, pk=pk)
    ProductAttributeFormSet = inlineformset_factory(BrickProduct, ProductAttribute, fields=('name', 'dimensions', 'price', 'stock'), extra=1)

    if request.method == 'POST':
        form = BrickProductForm(request.POST, instance=brick_product)
        formset = ProductAttributeFormSet(request.POST, instance=brick_product)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('all_items_list')  # Redirect to the list view after editing
    else:
        form = BrickProductForm(instance=brick_product)
        formset = ProductAttributeFormSet(instance=brick_product)

    context = {
        'forms': form,
        'formset': formset,
        'brick_product': brick_product,
    }
    return render(request, 'Inventory/Edit_product_Byid.html', context)

@login_required(login_url='login')
def sales_list(request):
    # Check if the user is a superuser
    if not request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    form =SalesForm()
    sale = Sale.objects.all()
    products = BrickProduct.objects.all()
    product_attributes = ProductAttribute.objects.all()

    if request.method == 'POST':
        form = SalesForm(request.POST)
        if form.is_valid():
            f_product_id = request.POST.get('product')
            f_product_attribute_name = request.POST.get('product_attribute')
            f_quantity_sold = request.POST.get('quantity_sold')
            
            # Retrieve product and filter product attribute by product_id and name
            f_product = BrickProduct.objects.get(id=f_product_id)
            f_product_attribute = get_object_or_404(ProductAttribute, product_id=f_product_id, name=f_product_attribute_name)

            new_sales = Sale.objects.create(
                product=f_product,
                product_attribute=f_product_attribute.id,
                quantity_sold=f_quantity_sold,
                date_sold=timezone.now(),
            )
            new_sales.save()
            return redirect('all_items_list')  # Redirect to the list view after editing
    else:
        form = SalesForm()
    context ={
        "forms":form,
        "sales":sale,
        "products": products,
        "product_attributes": product_attributes,
    }
    return render(request, 'Inventory/Sales_list_add.html', context)

@login_required(login_url='login')
def add_inventory(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to access this page.")

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
