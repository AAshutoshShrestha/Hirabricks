from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *

# Register your models here.
@admin.register(BrickProduct)
class BrickProductAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    def product_img_display(self, obj):
        # Call the soil_img_display method on the provided object
        return obj.product_img_display()

    product_img_display.short_description = 'Soil Image'

    list_display = ('id','product_code','name','category', 'description','dimensions','price','stock','product_img_display')
    list_filter = ('id', 'name','category','product_code',)
    search_fields = ('id', 'name','category','product_code',)
    list_per_page = 15


@admin.register(BrickCategory)
class BrickCategoryAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('id','name','slug')
    list_filter = ('name',)
    search_fields = ('name',)
    list_per_page = 15

@admin.register(Sale)
class SaleAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('id','product','quantity_sold','date_sold')
    list_filter = ('id','product',)
    search_fields = ('id','product',)
    list_per_page = 15