from django.urls import path
from .views import *

from graphene_django.views import GraphQLView
from .schema import schema


urlpatterns = [
    path('', inventory, name='inventory'),
    path('all-products/', all_items_list, name='all_items_list'),
    path('edit/<int:pk>/', product_edit, name='product_edit'),
    path('sales/', sales_list, name='sales_list'),
    path('add-inventory/', add_inventory, name='add_inventory'),

    path("api", GraphQLView.as_view(graphiql=True, schema=schema)),

]