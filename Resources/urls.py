from django.urls import path
from .views import *

urlpatterns = [
    path('resource-form/', coals, name='resource_form'),
    path('resource-reports/', reports, name='resource_reports'),
]
