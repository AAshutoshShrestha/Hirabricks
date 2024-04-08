from django.urls import path
from .views import *

urlpatterns = [
    path('machineRunTime', machine_status_update, name='machine_runtime'),
    path('Runtime-records', runtime_records, name='runtime_records'),
    path('maintenance/', maintenance_tasks, name='maintenance_tasks'),
    path('update-task/<int:pk>/', update_task_status, name='update_task_status'),
    path('delete-task/<int:pk>/', delete_task, name='task_delete'),

]