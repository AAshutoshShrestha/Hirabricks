from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
from import_export import resources, fields
import logging

logger = logging.getLogger(__name__)


@admin.register(BurnerConsumption)
class BurnerConsumptionAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('id','date','coal_weight','burner_number')
    list_filter = ('burner_number',)
    search_fields = ('burner_number',)
    list_per_page = 15

@admin.register(JhogaiConsumption)
class JhogaiConsumptionAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('id','date','type','weight')
    list_filter = ('type',)
    search_fields = ('type',)
    list_per_page = 15



class SoilDetailsResource(resources.ModelResource):
    export_soil_img = fields.Field(attribute='export_soil_img')
    export_Soil_testrep = fields.Field(attribute='export_Soil_testrep')

    class Meta:
        model = SoilDetails
        fields = ['id',  'date','user', 'type','Source','sand','silt','clay','remarks', 'export_soil_img','export_Soil_testrep']


@admin.register(SoilDetails)
class SoilDetailsAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    resource_class = SoilDetailsResource
    def soil_img_display(self, obj):
        # Call the soil_img_display method on the provided object
        return obj.soil_img_display()

    soil_img_display.short_description = 'Soil Image'

    def soil_test_report_display(self, obj):
        # Call the soil_img_display method on the provided object
        return obj.soil_test_report_display()

    soil_test_report_display.short_description = 'Soil Test Image'

    list_display = ('id',  'date','user', 'type','Source','sand','silt','clay','remarks', 'soil_img_display','soil_test_report_display')
    list_filter = ('id', 'date',)
    search_fields = ('id', 'date')
    list_per_page = 15