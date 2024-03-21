from django.urls import path
from .views import *

urlpatterns = [
    path('', inventory, name='inventory'),
    path('all-products/', all_items_list, name='all_items_list'),
    path('edit/<int:pk>/', product_edit, name='product_edit'),
    ]