from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *

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

@admin.register(SoilDetails)
class SoilDetailsAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    def soil_img_display(self, obj):
        # Call the soil_img_display method on the provided object
        return obj.soil_img_display()

    soil_img_display.short_description = 'Soil Image URL'

    def save_model(self, request, obj, form, change):
        # Call the parent class's save_model method to save the model instance
        super().save_model(request, obj, form, change)

        # Check if a soil image is provided
        if 'soil_img' in request.FILES:
            soilimg = request.FILES.get('soil_img')

            # Check if the uploaded file is not empty
            if soilimg.size == 0:
                logger.error("Uploaded soil image is empty")
                # Handle the error or raise an exception accordingly
                return

            # Check if the uploaded file is an image
            if not soilimg.content_type.startswith('image'):
                logger.error("Uploaded file is not an image")
                # Handle the error or raise an exception accordingly
                return

            # Upload the soil image to Supabase storage
            res = supabase.storage.from_('image-bucket').upload(soilimg.name, soilimg.read(), {'content-type': 'image/jpeg'})

            # Check the type of the response
            if isinstance(res, dict):
                obj.soil_img = res['url']  # Save the URL of the uploaded image
                obj.save()
            else:
                logger.error(f"Error uploading soil image: {res}")
                # Handle the error or raise an exception accordingly

    list_display = ('id', 'user', 'date', 'type', 'sand', 'silt', 'clay', 'remarks', 'soil_img_display')
    list_filter = ('id', 'date',)
    search_fields = ('id', 'date')
    list_per_page = 15