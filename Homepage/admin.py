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

@admin.register(Company_info)
class Company_infoAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('id','name','address','phone_number','email')
    list_filter = ('id','name','address','phone_number',)
    search_fields = ('id','name','address','phone_number',)
    list_per_page = 15

@admin.register(SocialLink)
class SocialLinkAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('id','name','url','icon')
    list_filter = ('id','name',)
    search_fields = ('id','name',)
    list_per_page = 15

@admin.register(TeamMember)
class TeamMemberAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('id','name','position','image_url')
    list_filter = ('id','name',)
    search_fields = ('id','name',)
    list_per_page = 15
