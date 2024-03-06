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
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        thermocouples = Thermocouple.objects.all()
        for thermocouple in thermocouples:
            field_name = thermocouple.name.lower().replace(" ", "_")
            form.base_fields[field_name] = forms.IntegerField(required=False)  # Fix the NameError here by referring to forms
        return form

    list_display = ['id','date', 'time','user']
    list_filter = ('id',)
    search_fields = ('id',)
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