from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *

from example.models import Car,Firing


@login_required(login_url='login')
def required_conditions(request):
    first_firing_zone = Firing.objects.first()
    try:
        # car = Car.objects.get(zone_id=18)  # Retrieve the car with zone id 18
        car = Car.objects.get(zone_id=first_firing_zone.zone_id)  # Retrieve the car with zone id 18
        cond_type = car.Type # Retrieve the Type of car with zone id 18
        req_condition = condition.objects.get(name=cond_type.name)  # Retrieve the condition associated with the car
        
    except Car.DoesNotExist:
        req_condition = None  # Set req_condition to None if car is not found
    except condition.DoesNotExist:
        req_condition = None  # Set req_condition to None if condition is not found

    context = {
        'req_condition': req_condition, 
    }
    return context