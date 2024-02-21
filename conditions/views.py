from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *

from example.models import Car,Firing


@login_required(login_url='login')
def required_MultiConditions(request):
    first_firing_zone = Firing.objects.first()
    Condition = MultiCondition.objects.all()
    try:
        car = Car.objects.get(zone_id=first_firing_zone.zone_id)  # Retrieve the car with firing zone id 
        cond_type = car.Type # Retrieve the Type of car product int that zone
        req_MultiCondition = MultiCondition.objects.get(name=cond_type.name)  # Retrieve the MultiCondition associated with the car product
        
    except Car.DoesNotExist:
        req_MultiCondition = None  # Set req_MultiCondition to None if car is not found

    context = {
        'req_condition': req_MultiCondition, 
        'Condition': Condition, 
    }
    return context

def foranalytics(request):
    single_MultiConditions = MultiCondition.objects.filter(is_multi_type=False)
    multi_MultiConditions = MultiCondition.objects.filter(is_multi_type=True)
    
    single_data = [{'name': cond.name, 'capacity': cond.capacity} for cond in single_MultiConditions]
    multi_data = [{'name': cond.name, 'items': [{'name': item.name, 'capacity': item.capacity} for item in cond.items.all()]} for cond in multi_MultiConditions]
    
    context = {
        'single_data': single_data,
        'multi_data': multi_data,
    }
    
    return context
