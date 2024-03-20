from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *

# Register your models here.

@admin.register(ContactMessage)
class ContactMessageAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('id','name','email','message','created_at')
    list_filter = ('id','name','email','created_at',)
    search_fields = ('id','name','email','created_at',)
    list_per_page = 15
