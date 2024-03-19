from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from .models import *

@admin.register(MachineArea)
class MachineAreaAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['id','name','area']
    list_filter = ('name',)
    search_fields = ('name',)
    list_per_page = 15

@admin.register(Machine)
class MachineAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['id','machine_area','name']
    list_filter = ('id','machine_area',)
    search_fields = ('machine_area','name',)
    list_per_page = 15



@admin.register(MachineOperator)
class Machine_ControlerAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['id','user','name']
    list_filter = ('user','name',)
    search_fields = ('user','name',)
    list_per_page = 15


class MachineRuntimeResource(resources.ModelResource):
    Machine_name = fields.Field(attribute='Machine_name')
    Worked_hours = fields.Field(attribute='Worked_hours')

    class Meta:
        model = MachineRuntime
        fields = ('id', 'start_time', 'end_time', 'machine_operator', 'Machine_name', 'Worked_hours')


@admin.register(MachineRuntime)
class MachineRuntimeAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    resource_class = MachineRuntimeResource

    list_display = ('id', 'Machine_name', 'machine_operator','start_time', 'end_time','Worked_hours','not_working','reason')
    list_filter = ('id','start_time',)
    search_fields = ('id','machine_operator__machine__name',)
    list_per_page = 15

@admin.register(MaintenanceTask)
class MaintenanceTaskAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('id','area','machine', 'title', 'description', 'status',)
    list_filter = ('id','title', 'status',)
    search_fields = ('id','title', 'status',)
    list_per_page = 15