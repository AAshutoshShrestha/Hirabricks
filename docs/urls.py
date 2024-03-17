from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', docs, name='docs'),
    path('developers/<slug:slug>/', dev, name='dev'),
    path('users/<slug:slug>/', users, name='users'),
    path('System-Administrator/<slug:slug>/', sys_admin, name='sys_admin'),

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
