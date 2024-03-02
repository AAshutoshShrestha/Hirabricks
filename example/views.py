from django.shortcuts import render, redirect
from django.utils import timezone

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm

from django.db.models import Count,F, ExpressionWrapper, fields

from datetime import timedelta, date

from .decorators import unauthenticated_user
from .forms import CarEntryForm,TemperatureInputForm
from .models import *
from conditions.models import MultiCondition
from conditions.views import required_MultiConditions,foranalytics

import locale

# Set the locale to the user's default setting
locale.setlocale(locale.LC_ALL, '')


def convert_to_hours_and_minutes(value):
    hours = value // 60
    minutes = value % 60
    return f"{hours} hours, {minutes} minutes"

def format_timedelta(td):
    total_minutes = td.days * 24 * 60 + td.seconds // 60
    hours, minutes = divmod(total_minutes, 60)

    parts = []
    if hours:
        parts.append(f"{hours} hours")
    if minutes:
        parts.append(f"{minutes} minutes")

    return ', '.join(parts)


def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
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
    cars = Car.objects.select_related('zone', 'Type').exclude(zone_id=None).order_by('zone')
    completed_cars = Car.objects.filter(status='COMPLETED').select_related('zone', 'Type').order_by('zone')

    req_MultiConditions_context = required_MultiConditions(request)

    if request.method == 'POST':
        carform = CarEntryForm(request.POST)
        if carform.is_valid():
            car_number = request.POST.get('car_number')
            remarks = request.POST.get('remarks')
            MultiCondition_instance = MultiCondition.objects.get(id=request.POST.get('Type'))
            existing_car_inline = Car.objects.filter(car_number=car_number, status='INLINE').exists()
            if existing_car_inline:
                carform.add_error(None, "A car with the same car number is already in line.")

            total_zones = Zone.objects.count()
            last_car_in_last_zone = Car.objects.filter(zone_id=total_zones).last()
            if last_car_in_last_zone:
                last_car_in_last_zone.zone_id = None
                last_car_in_last_zone.exit_time = timezone.now()
                last_car_in_last_zone.status = 'COMPLETED'
                last_car_in_last_zone.save()

            Car.objects.filter(zone_id__lt=total_zones).update(zone_id=F('zone_id') + 1)

            zone_id = 1
            status = 'INLINE'
            by = request.user
            
            car = Car.objects.create(
                user=by,
                zone_id=zone_id,
                Type=MultiCondition_instance,
                car_number=car_number,
                entry_time=timezone.now(),
                exit_time=None,
                status=status,
                remarks=remarks,
            )
            car.save()

            request.session['success_message'] = "New Car added successfully"
            return redirect('index')
    else:
        carform = CarEntryForm()

    context = {
        **req_MultiConditions_context,
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
                TemperatureRecord.objects.create(
                    date=current_datetime.date(),
                    time=current_datetime.time(),
                    temperature=temperature_value,
                    thermocouple=thermocouple
                )

            return redirect('dashboard')

    context = {'tempform': form}
    return render(request, 'index.html', context)



@login_required(login_url='login')
def analytics(request):
    # Query for single and multi-type conditions
    single_MultiConditions = MultiCondition.objects.filter(is_multi_type=False)
    multi_MultiConditions = MultiCondition.objects.filter(is_multi_type=True)
    
    # Prepare data for single and multi-type conditions
    single_data = [{'name': cond.name, 'capacity': cond.capacity} for cond in single_MultiConditions]
    multi_data = [{'name': cond.name, 'items': [{'name': item.name, 'capacity': item.capacity} for item in cond.items.all()]} for cond in multi_MultiConditions]

    # Query for required analytics data
    firezone = Firing.objects.all().count()
    type_counts = dict(
        MultiCondition.objects.annotate(count=Count('car__Type')).order_by('id').values_list('name', 'count')
    )
    capacities = dict(MultiCondition.objects.order_by('id').values_list('name', 'capacity'))

    # Calculate combined totals for single and multi type conditions
    single_type_total = sum(items['capacity'] * type_counts.get(items['name'], 0) for items in single_data)
    multi_type_total = sum(subitem['capacity'] * type_counts.get(items['name'], 0) for items in multi_data for subitem in items['items'])

    combined_total = single_type_total+multi_type_total

    formatted_combined_total = locale.format_string("%d", combined_total, grouping=True)

    req_MultiConditions_context = required_MultiConditions(request)
    
    current_date = date.today()
    Todays_total_push = Car.objects.filter(entry_time__date=current_date).count()
    Total_push = Car.objects.all().count()

    yesterday = date.today() - timedelta(days=1)
    yesterday_total_push = Car.objects.filter(entry_time__date=yesterday).count()

    push_counts=Car.objects.values('entry_time__date').annotate(push_count=Count('id')).order_by('-entry_time__date')

    all_data = Car.objects.all().order_by('id')

    context = {
        **req_MultiConditions_context,
        'single_data': single_data,
        'multi_data': multi_data,
        'Todays_total_push': Todays_total_push,
        'yesterday_total_push': yesterday_total_push,
        'Total_push': Total_push,
        'firezone': firezone,
        'alldatas': all_data,
        'type_counts': type_counts,
        'push_counts': push_counts,
        'capacities': capacities,
        'combined_total': formatted_combined_total,

    }
    return render(request, 'analytics.html', context)


@login_required(login_url='login')
def profile(request):
    car_count = Car.objects.filter(user=request.user).count()
    context = {'Car_count': car_count}
    return render(request, 'profile.html', context)


@login_required(login_url='login')
def history(request):
    completed_cars = Car.objects.filter(status='COMPLETED').order_by('-id')
    for car in completed_cars:
        cycle_time = car.exit_time - car.entry_time
        car.cycle_time = format_timedelta(cycle_time)

    context = {'Completed': completed_cars}
    return render(request, 'history.html', context)

@login_required(login_url='login')
def alldatas(request):
    all_data = Car.objects.all().z('zone', 'Type').order_by('zone')
    for car in all_data:
        if car.exit_time is not None:
            cycle_time = car.exit_time - car.entry_time
            car.cycle_time = format_timedelta(cycle_time)
        else:
            car.cycle_time = "--"
            
    context = {'alldatas': all_data}
    return render(request, 'alldatas.html', context)

@login_required(login_url='login')
def test(request):
    # Query for single and multi-type conditions
    single_MultiConditions = MultiCondition.objects.filter(is_multi_type=False)
    multi_MultiConditions = MultiCondition.objects.filter(is_multi_type=True)
    
    # Prepare data for single and multi-type conditions
    single_data = [{'name': cond.name, 'capacity': cond.capacity} for cond in single_MultiConditions]
    multi_data = [{'name': cond.name, 'items': [{'name': item.name, 'capacity': item.capacity} for item in cond.items.all()]} for cond in multi_MultiConditions]

    # Query for required analytics data
    firezone = Firing.objects.all().count()
    type_counts = dict(
        MultiCondition.objects.annotate(count=Count('car__Type')).order_by('id').values_list('name', 'count')
    )
    capacities = dict(MultiCondition.objects.order_by('id').values_list('name', 'capacity'))

    # Calculate combined totals for single and multi type conditions
    single_type_total = sum(items['capacity'] * type_counts.get(items['name'], 0) for items in single_data)
    multi_type_total = sum(subitem['capacity'] * type_counts.get(items['name'], 0) for items in multi_data for subitem in items['items'])
    combined_total = single_type_total+multi_type_total

    formatted_combined_total = locale.format_string("%d", combined_total, grouping=True)

    req_MultiConditions_context = required_MultiConditions(request)
    
    current_date = date.today()
    Todays_total_push = Car.objects.filter(entry_time__date=current_date).count()
    Total_push = Car.objects.all().count()

    yesterday = date.today() - timedelta(days=1)
    yesterday_total_push = Car.objects.filter(entry_time__date=yesterday).count()

    push_counts=Car.objects.values('entry_time__date').annotate(push_count=Count('id')).order_by('entry_time__date')

    all_data = Car.objects.all().order_by('id')

    context = {
        **req_MultiConditions_context,
        'single_data': single_data,
        'multi_data': multi_data,
        'Todays_total_push': Todays_total_push,
        'yesterday_total_push': yesterday_total_push,
        'Total_push': Total_push,
        'firezone': firezone,
        'alldatas': all_data,
        'type_counts': type_counts,
        'push_counts': push_counts,
        'capacities': capacities,
        'combined_total': formatted_combined_total,
    }
    return render(request, 'test.html', context)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'updatepassword.html', {'form': form})