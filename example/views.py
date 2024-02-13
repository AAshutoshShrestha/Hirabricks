from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta, date
from django.core import serializers
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


from .decorators import unauthenticated_user
from .forms import CarEntryForm,TemperatureInputForm
from .models import *
from conditions.models import *
from conditions.views import required_conditions


def convert_to_hours_and_minutes(value):
    hours = value // 60
    minutes = value % 60
    return f"{hours} hours, {minutes} minutes"

@unauthenticated_user
def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('index')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
def index(request):
    firing = Firing.objects.all()
    cars = Car.objects.exclude(zone_id=None).order_by('zone')
    completed_cars = Car.objects.filter(status='COMPLETED').order_by('zone')

    req_conditions_context = required_conditions(request)

    # Check if the form is submitted (POST request)
    if request.method == 'POST':
        # Create form instance and validate data
        carform = CarEntryForm(request.POST)
        if carform.is_valid():
            # Get the new car number from the form
            car_number = request.POST.get('car_number')
            remarks = request.POST.get('remarks')

            Type = request.POST.get('Type')
            condition_instance = condition.objects.get(id=Type)

            # Check if a car with the same car number and status 'INLINE' exists
            existing_car_inline = Car.objects.filter(car_number=car_number, status='INLINE').exists()
            if existing_car_inline:
                carform.add_error(None, "A car with the same car number is already in line.")
                
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
            by =request.user
            
            # Create the new car
            car = Car.objects.create(
                user =by,
                zone_id=zone_id,
                Type=condition_instance,
                car_number=car_number,
                entry_time=timezone.now(),
                exit_time=None,
                status=status,
                remarks=remarks,
            )
            car.save()


            # Redirect to the same form page after successful submission
            request.session['success_message'] = "New Car added succesfully"
            return redirect('index') 
    else:
        # For GET request, create a new form instance
        carform = CarEntryForm()

    context = {
        **req_conditions_context,
        'carForm': carform,
        'Cars': cars,
        'firing': firing,
        'Completed': completed_cars,
    }
    return render(request, 'index.html', context)


@login_required(login_url='login')
def forms(request):
    form = TemperatureInputForm()
    if request.method == 'POST':
        form = TemperatureInputForm(request.POST)
        if form.is_valid():
            current_datetime = timezone.now()

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
    return render(request, 'index.html', context)

@login_required(login_url='login')
def history(request):
    completed_cars = Car.objects.filter(status='COMPLETED').order_by('id')
    context={
        'Completed': completed_cars, 
    }
    return render(request, 'history.html', context)
    
@login_required(login_url='login')
def analytics(request):
    firezone = Firing.objects.all().count()

    # get stats of todays total car entry 
    current_date = date.today()
    Todays_total_push = Car.objects.filter(entry_time__date=current_date).count()
    Total_push = Car.objects.all().count()

    # Get yesterday's date
    yesterday = date.today() - timedelta(days=1)
    yesterday_total_push = Car.objects.filter(entry_time__date=yesterday).count()


    all = Car.objects.all().order_by('id')
    context={
        'Todays_total_push': Todays_total_push,
        'yesterday_total_push': yesterday_total_push,
        'Total_push': Total_push,
        'firezone': firezone,
        'alldatas': all,
    }
    return render(request, 'analytics.html', context)

@login_required(login_url='login')
def profile(request):
    Car_count = Car.objects.filter(user=request.user).count()

    context={
        'Car_count': Car_count, 
    }
    return render(request, 'profile.html', context)
    
@login_required(login_url='login')
def alldatas(request):
    alldatas = Car.objects.all().order_by('zone')
    context={
        'alldatas': alldatas, 
    }
    return render(request, 'alldatas.html', context)

@login_required(login_url='login')
def test(request):
    firing = Firing.objects.all()
    
    fire_instance = Firing.objects.first()
    fire_zone_id = fire_instance.id

    cars = Car.objects.exclude(zone_id=None).order_by('zone')
    completed_cars = Car.objects.filter(status='COMPLETED').order_by('zone')
    carform = CarEntryForm(request.POST)
    req_conditions_context = required_conditions(request)

    duration = req_conditions_context.Durations()
    converted =convert_to_hours_and_minutes(duration)
    context = {
        **req_conditions_context,
        'carForm': carform,
        'converted': converted,
        'Cars': cars,
        'firing': firing,
        'fire_zone_id': fire_instance,
        'Completed': completed_cars,
    }
    return render(request, 'test.html', context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'updatepassword.html', {
        'form': form
    })