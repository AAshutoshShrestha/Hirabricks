from django.urls import path
from .views import *

urlpatterns = [
    path('machineRunTime', record_time, name='machine_runtime'),
    path('Runtime-records', runtime_records, name='runtime_records'),
]