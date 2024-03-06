from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django import forms

from .models import Thermocouple, Zone, Car,TemperatureRecord,Firing

@admin.register(Thermocouple)
class ThermocoupleAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['name']
    list_filter = ('name',)
    search_fields = ('name',)
    list_per_page = 15






# Custom form for TemperatureRecordAdmin
class TemperatureRecordForm(forms.ModelForm):
    class Meta:
        model = TemperatureRecord
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Dynamically add fields for Thermocouple objects
        thermocouples = Thermocouple.objects.all()
        for thermocouple in thermocouples:
            field_name = thermocouple.name.lower().replace(" ", "_")
            self.fields[field_name] = forms.IntegerField(required=False)


@admin.register(TemperatureRecord)
class TemperatureRecordAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    form = TemperatureRecordForm
    list_display = ['id', 'date', 'time', 'user']

    # Dynamically add Thermocouple fields to list_display
    thermocouples = Thermocouple.objects.all()
    for thermocouple in thermocouples:
        field_name = thermocouple.name.lower().replace(" ", "_")
        list_display.append(field_name)

    list_filter = ['date', 'time']
    search_fields = ['id']
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