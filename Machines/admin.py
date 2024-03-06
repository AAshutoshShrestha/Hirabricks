from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import *

@admin.register(Machine)
class MachineAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['id','name','area']
    list_filter = ('name',)
    search_fields = ('name',)
    list_per_page = 15

@admin.register(MachineOperator)
class Machine_ControlerAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['id','user','name']
    list_filter = ('user','name',)
    search_fields = ('user','name',)
    list_per_page = 15

@admin.register(MachineRuntime)
class MachineRuntimeAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('id', 'machine_name', 'machine_operator','start_time', 'end_time','Worked_hours')
    list_filter = ('id','start_time',)
    search_fields = ('id','machine_operator__machine__name',)
    list_per_page = 15