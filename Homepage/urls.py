from django.urls import path
from .views import *

urlpatterns = [
    path('', main, name='homepage'),
    path('products/', all_products, name='products'),
    path('products/<slug:slug>', product_detail, name='product_detail'),
    path('category/<slug:slug>', By_category, name='By_category'),
    path('gallery/', gallery, name='gallery'),
]