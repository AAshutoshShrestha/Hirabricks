from django.contrib.auth.decorators import login_required
from .models import *
from example.models import Car, Firing

@login_required(login_url='login')
def required_MultiConditions(request):
    """
    Retrieve required MultiConditions based on certain conditions.

    Args:
        request: HttpRequest object.

    Returns:
        Dictionary containing context data.
    """
    # Retrieve the first firing zone
    first_firing_zone = Firing.objects.first()
    
    # Retrieve all MultiConditions
    Condition = MultiCondition.objects.all()
    
    try:
        # Retrieve the car associated with the firing zone id
        car = Car.objects.get(zone_id=first_firing_zone.zone_id)
        
        # Retrieve the Type of car product in that zone
        cond_type = car.Type 
        
        # Retrieve the MultiCondition associated with the car product
        req_MultiCondition = MultiCondition.objects.get(name=cond_type.name)
        
    except Car.DoesNotExist:
        req_MultiCondition = None  # Set req_MultiCondition to None if car is not found

    # Define context data
    context = {
        'req_condition': req_MultiCondition, 
        'Condition': Condition, 
    }
    return context

@login_required(login_url='login')
def foranalytics(request):
    """
    Prepare data for analytics.

    Args:
        request: HttpRequest object.

    Returns:
        Dictionary containing context data.
    """
    # Filter MultiConditions based on single and multi type
    single_MultiConditions = MultiCondition.objects.filter(is_multi_type=False)
    multi_MultiConditions = MultiCondition.objects.filter(is_multi_type=True)
    
    # Prepare data for single and multi type MultiConditions
    single_data = [{'name': cond.name, 'capacity': cond.capacity} for cond in single_MultiConditions]
    multi_data = [{'name': cond.name, 'items': [{'name': item.name, 'capacity': item.capacity} for item in cond.items.all()]} for cond in multi_MultiConditions]
    
    # Define context data
    context = {
        'single_data': single_data,
        'multi_data': multi_data,
    }
    
    return context
