from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *

from example.models import Car,Firing


@login_required(login_url='login')
def required_conditions(request):
    first_firing_zone = Firing.objects.first()
    try:
        car = Car.objects.get(zone_id=first_firing_zone.zone_id)  # Retrieve the car with firing zone id 
        cond_type = car.Type # Retrieve the Type of car product int that zone
        req_condition = condition.objects.get(name=cond_type.name)  # Retrieve the condition associated with the car product
        
    except Car.DoesNotExist:
        req_condition = None  # Set req_condition to None if car is not found

    context = {
        'req_condition': req_condition, 
    }
    return context