from django.urls import path
from .views import *

urlpatterns = [
    path('', main, name='homepage'),
    path('products/', products, name='products'),
    path('products/<slug:slug>', product_detail, name='product_detail'),
    path('category/<str:category_id>', By_category, name='By_category'),
]