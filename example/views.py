
from django.shortcuts import render, redirect,HttpResponse
from django.db.models import Max
from django.utils import timezone
from django.core import serializers
from .forms import CarEntryForm,TemperatureInputForm
from .models import *

def index(request):
    cars = Car.objects.exclude(zone_id=None).order_by('zone')
    completed_cars = Car.objects.filter(status='COMPLETED').order_by('zone')

    # Check if the form is submitted (POST request)
    if request.method == 'POST':
        # Create form instance and validate data
        carform = CarEntryForm(request.POST)
        if carform.is_valid():
            # Get the new car number from the form
            car_number = carform.cleaned_data['car_number']

            # Find the total number of zones created by the admin
            total_zones = Zone.objects.count()

            # Update zone IDs for existing cars till the last zone
            for existing_car in Car.objects.all():
                if existing_car.zone_id is not None and existing_car.zone_id < total_zones:
                    existing_car.zone_id += 1
                    existing_car.save()
                else:
                    existing_car.zone_id = None  # Set zone_id to None for the last zone
                    existing_car.exit_time = timezone.now()
                    existing_car.status = 'COMPLETED'
                    existing_car.save()

            # Assign the new car to the first zone
            zone_id = 1
            status = 'INLINE'
            
            # Create the new car
            car = Car.objects.create(
                zone_id=zone_id,
                car_number=car_number,
                entry_time=timezone.now(),
                exit_time=None,
                status=status
            )

            # Redirect to the same form page after successful submission
            return redirect('index') 
    else:
        # For GET request, create a new form instance
        carform = CarEntryForm()

    context = {
        'carForm': carform,
        'Cars': cars,
        'Completed': completed_cars,
    }
    return render(request, 'index.html', context)


    
def forms(request):
    form = TemperatureInputForm()
    if request.method == 'POST':
        form = TemperatureInputForm(request.POST)
        if form.is_valid():
            current_datetime = timezone.now().strftime("%H:%M:%S %Y-%m-%d ")

            for thermocouple in Thermocouple.objects.all():
                field_name = f"temperature_{thermocouple.id}"
                temperature_value = form.cleaned_data.get(field_name)

                # Create a TemperatureRecord object for each Thermocouple
                TemperatureRecord.objects.create(
                    date=current_datetime.split()[0],
                    time=current_datetime.split()[1],
                    temperature=temperature_value,
                    thermocouple=thermocouple
                )

            object_list = serializers.serialize("python", Thermocouple.objects.all())

            for object in object_list:
                for i, field_value in object['fields'].items():
                        print (i, field_value)
            return redirect('dashboard')

    else:
        form = TemperatureInputForm()
    
    context={
        'tempform': form, 
    }
    return render(request, 'forms.html', context)

def dashboard(request):
    completed_cars = Car.objects.filter(status='COMPLETED').order_by('zone')
    context={
        'Completed': completed_cars, 
    }
    return render(request, 'dashboard.html', context)