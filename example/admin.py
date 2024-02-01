from django.contrib import admin
from .models import Thermocouple, Zone, Car,TemperatureRecord

@admin.register(Thermocouple)
class ThermocoupleAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(TemperatureRecord)
class TemperatureRecordAdmin(admin.ModelAdmin):
    list_display = ['id','date', 'thermocouple','temperature']

@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'thermocouple']

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['zone','car_number', 'entry_time','status']
    search_fields = ['car_number']