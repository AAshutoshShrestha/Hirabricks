from django.urls import path
from .views import *

urlpatterns = [
    path('', main, name='homepage'),
    path('products/', products, name='products'),
    path('products/<int:product_id>', product_detail, name='product_detail'),
]