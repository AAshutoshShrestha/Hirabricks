from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('resource-form/', coals, name='resource_form'),
    path('todays-records/', todaysRecord, name='todays_record'),
    path('resource-reports/', reports, name='resource_reports'),
    path('soil-form/', soil_mixture, name='soil_mixture'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

