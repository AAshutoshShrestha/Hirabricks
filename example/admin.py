from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Thermocouple, Zone, Car,TemperatureRecord,Firing

@admin.register(Thermocouple)
class ThermocoupleAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['name']
    list_filter = ('name',)
    search_fields = ('name',)
    list_per_page = 15

@admin.register(TemperatureRecord)
class TemperatureRecordAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['id','date', 'thermocouple','temperature']
    list_filter = ('id',)
    search_fields = ('thermocouple',)
    list_per_page = 15

@admin.register(Zone)
class ZoneAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['id','name', 'thermocouple','area']
    list_filter = ('id',)
    search_fields = ('name',)
    list_per_page = 15

@admin.register(Firing)
class FiringAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['id','zone']
    list_filter = ('id',)
    search_fields = ('zone',)
    list_per_page = 15

@admin.register(Car)
class CarAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['zone','car_number', 'entry_time','exit_time','Type','status']
    list_filter = ('id','Type',)
    search_fields = ('zone',)
    list_per_page = 15