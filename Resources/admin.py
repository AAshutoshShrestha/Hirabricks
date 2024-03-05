from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
from django.utils.html import format_html

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

@admin.register(SoilDetails)
class SoilDetailsAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('id','user','date','type','sand','silt','clay','remarks','soil_img')
    list_filter = ('id','date',)
    search_fields = ('id','date')
    list_per_page = 15