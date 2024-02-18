from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import condition

@admin.register(condition)
class conditionsAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('name','Fan_Speed','Dryer_Speed','Burner_Speed','Temperature','Durations')
    list_filter = ('name',)
    search_fields = ('name',)
    list_per_page = 15

