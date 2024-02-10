from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    # path('dashboard/', dashboard, name='dashboard'),
    path('history/', history, name='history'),
    path('alldatas/', alldatas, name='alldatas'),
    path('analytics/', analytics, name='analytics'),
    path('profile/', profile, name='profile'),
    path('test/', test, name='test'),

    path('login/', loginPage, name="login"),  
	path('logout/', logoutUser, name="logout"),
	path('change_password/', change_password, name="change_password"),
    
]
