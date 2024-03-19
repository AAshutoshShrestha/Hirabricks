from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from django.views.static import serve
from vercel_app.utils import export_csv

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Homepage.urls')),
    path('Conditions/', include('conditions.urls')),
    path('Dashboard/', include('example.urls')),
    path('Machine/', include('Machines.urls')),
    path('Resources/', include('Resources.urls')),
    path('docs/', include('docs.urls')),
    path('inventory/', include('Inventory.urls')),

    path('export-csv/', export_csv, name='export_csv'),
    
    re_path(r'^static/(?P<path>.*)$', serve, {
            'document_root': settings.STATIC_ROOT,
        }),
    re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
]

handler404 = "example.views.page_not_found_view"