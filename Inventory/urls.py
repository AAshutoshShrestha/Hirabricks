from django.urls import path
from .views import *

urlpatterns = [
    path('', inventory, name='inventory'),
    ]