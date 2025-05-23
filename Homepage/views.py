from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ContactForm
from .models import *
from Inventory.models import BrickProduct, BrickCategory    

# Importing environment variables
import os
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Supabase client
url = os.environ.get('SUPABASE_URL')
key = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
supabase = create_client(url, key)

def main(request):
    """
    View for the main page.

    Args:
        request: HttpRequest object.

    Returns:
        Rendered template for the main page with context data.
    """
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
        'form': form,
    }
    return render(request, 'Main/home.html', context)

def all_products(request):
    """
    View for displaying all products.

    Args:
        request: HttpRequest object.

    Returns:
        Rendered template for displaying all products with context data.
    """
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
    """
    View for displaying products by category.

    Args:
        request (HttpRequest): The HTTP request object.
        slug (str): The slug of the category.

    Returns:
        HttpResponse: Rendered template for displaying products by category with context data.
    """
    # Get the category object or return 404 if not found
    category = get_object_or_404(BrickCategory, slug=slug)
    category_name = category

    # Query products belonging to the specified category
    product_by_category = BrickProduct.objects.filter(category=category).order_by('id')

    # Pagination
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
    
    # Fetch public URLs for product images from Supabase Storage
    for bricks in products:
        # Get public URL for product_image
        res = supabase.storage.from_('Products_image').get_public_url(bricks.product_image)
        # Update product_image field with the public URL
        bricks.product_image = res
    
    # Context data to pass to the template
    context = {
        'products': products,
        'category_empty': category_empty,
        'category': category_name,
    }

    # Render the template with the context data
    return render(request, 'Main/category.html', context)

def product_detail(request, slug):
    """
    View for displaying product details.

    Args:
        request: HttpRequest object.
        slug: Product slug.

    Returns:
        Rendered template for displaying product details with context data.
    """
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
    """
    View for displaying gallery of product images.

    Args:
        request: HttpRequest object.

    Returns:
        Rendered template for displaying gallery with context data.
    """

    object_names = supabase.storage.from_('Products_image').list()
    all_names = [name['name'] for name in object_names]

    paginator = Paginator(all_names, 12)  # 12 products per page

    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_obj = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_obj = paginator.page(paginator.num_pages)
    # Generate individual public URLs for each image in the current page
    individual_public_urls = [
        f"https://govmngfhcfddnuqorust.supabase.co/storage/v1/object/public/Products_image/{name}"
        for name in page_obj.object_list
    ]

    context = {
        'images': individual_public_urls,
        'page_obj': page_obj,
    }
    return render(request, 'Main/gallery.html', context)
