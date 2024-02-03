from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('dashboard/', dashboard, name='dashboard'),

    path('login/', loginPage, name="login"),  
	path('logout/', logoutUser, name="logout"),
]
