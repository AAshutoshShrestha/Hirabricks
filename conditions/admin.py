from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import MultiCondition,MultiItem

class MultiItemInline(admin.TabularInline):
    model = MultiItem

@admin.register(MultiCondition)
class MultiConditionAdmin(admin.ModelAdmin):
    list_display = ('name','fan_speed','dryer_speed','burner_speed','temperature','durations','capacity','is_multi_type')
    list_filter = ('name',)
    search_fields = ('name',)
    list_per_page = 15

    inlines = [MultiItemInline]

@admin.register(MultiItem)
class MultiItemAdmin(admin.ModelAdmin):
    list_display = ('multi_condition','name','capacity')
    list_filter = ('multi_condition',)
    search_fields = ('multi_condition',)
    list_per_page = 15