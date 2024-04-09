from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('history/', history, name='history'),
    path('alldatas/', alldatas, name='alldatas'),
    path('analytics/', analytics, name='analytics'),
    path('profile/', profile, name='profile'),
    path('temperature-forms/', temp_forms, name='temp_forms'),
    path('temperature-details/', temperature_details, name='temperature_details'),    
    path('login/', loginPage, name="login"),  
	path('logout/', logoutUser, name="logout"),
	path('change_password/', change_password, name="change_password"),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
