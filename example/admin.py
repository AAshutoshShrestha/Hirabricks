from django.contrib import admin
from import_export.admin import ImportExportMixin

from .models import Thermocouple, Zone, Car,TemperatureRecord

@admin.register(Thermocouple)
class ThermocoupleAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display = ['name']

@admin.register(TemperatureRecord)
class TemperatureRecordAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display = ['id','date', 'thermocouple','temperature']

@admin.register(Zone)
class ZoneAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display = ['id','name', 'thermocouple']

@admin.register(Car)
class CarAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display = ['zone','car_number', 'entry_time','exit_time','status']
    search_fields = ['zone']