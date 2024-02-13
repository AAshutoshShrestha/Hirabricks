from django.contrib import admin
from import_export.admin import ImportExportMixin

from .models import condition

@admin.register(condition)
class conditionsAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display = ('name','Fan_Speed','Dryer_Speed','Burner_Speed','Durations')
    list_filter = ('name',)
    search_fields = ('name',)
    list_per_page = 15

