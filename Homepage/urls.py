from django.urls import path
from graphene_django.views import GraphQLView
from .schema import schema
from .views import *

urlpatterns = [
    path('', main, name='homepage'),
    path('products/', all_products, name='products'),
    path('products/<slug:slug>', product_detail, name='product_detail'),
    path('category/<slug:slug>', By_category, name='By_category'),
    path('gallery/', gallery, name='gallery'),

    path("api", GraphQLView.as_view(graphiql=True, schema=schema)),
]