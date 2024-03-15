from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
from .forms import *

@admin.register(Post)
class PostAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['id','title','category','author','status','created_at','updated_at']
    list_filter = ('title',)
    search_fields = ('title',)
    list_per_page = 15
