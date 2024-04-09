import locale
import json
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, F, Sum
from django.db import connection
from datetime import timedelta, date

from conditions.models import MultiCondition
from conditions.views import required_MultiConditions, foranalytics
from Resources.models import *

from .decorators import unauthenticated_user
from .forms import CarEntryForm, TemperatureRecordForm
from .models import *
from .utils import format_timedelta

import pandas as pd
import plotly.express as px

# Set the locale to the user's default setting
locale.setlocale(locale.LC_ALL, '')

def convert_to_hours_and_minutes(value):
    """
    Convert time duration to hours and minutes format.

    Args:
        value (int): Time duration in minutes.

    Returns:
        str: Time duration in hours and minutes format.
    """
    hours = value // 60
    minutes = value % 60
    return f"{hours} hours, {minutes} minutes"

def page_not_found_view(request, exception):
    """
    Display custom 404 page.

    Args:
        request: HttpRequest object.
        exception: Exception object.

    Returns:
        Rendered template for 404 page.
    """
    return render(request, 'Auth/404.html', status=404)

@unauthenticated_user
def loginPage(request):
    """
    View for handling user login.

    Args:
        request: HttpRequest object.

    Returns:
        Rendered template for login page or redirects to index page.
    """
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
    return render(request, 'Auth/login.html', context)

def logoutUser(request):
    """
    Log out the user.

    Args:
        request: HttpRequest object.

    Returns:
        Redirect to login page.
    """
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def index(request):
    """
    View for the index page.

    Args:
        request: HttpRequest object.

    Returns:
        Rendered template for the index page with context data.
    """
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
def temperature_details(request):
    """
    View for temperature records details.

    Args:
        request: HttpRequest object.

    Returns:
        Rendered template for temperature records details with context data.
    """
    request.session['project_name'] = 'example'
    request.session['model_name'] = 'TemperatureRecord'

    temp_records = TemperatureRecord.objects.all()

    paginator = Paginator(temp_records, 50)  # 50 records per page
    page_number = request.GET.get('page')

    try:
        temp_data = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        temp_data = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        temp_data = paginator.page(paginator.num_pages)

    total = temp_records.count()
    context = {
        'temp_data': temp_data,
        'total': total,
    }
    return render(request, 'Temp_Records/Records.html', context)

@login_required(login_url='login')
def temp_forms(request):
    """
    View for temperature records forms.

    Args:
        request: HttpRequest object.

    Returns:
        Rendered template for temperature records forms with context data.
    """
    if request.method == 'POST':
        by = request.user
        form = TemperatureRecordForm(request.POST)
        if form.is_valid():
            last_record = TemperatureRecord.objects.last()  # Get the last record
            new_id = last_record.id + 1 if last_record else 1  # Increment the ID
            create = form.save(commit=False)
            create.id = new_id  # Assign the new ID
            create.user = by
            create.date = timezone.now().date()
            create.time = timezone.now().time()
            create.save()
            messages.success(request, "Kiln temperature recorded successfully")
            return redirect('temp_forms') 
    else:
        form = TemperatureRecordForm()

    context = {
        'tempform': form,
    }
    return render(request, 'Temp_Records/Forms.html', context)

@login_required(login_url='login')
def analytics(request):
    """
    View for analytics page.

    Args:
        request: HttpRequest object.

    Returns:
        Rendered template for analytics page with context data.
    """
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

    combined_total = single_type_total + multi_type_total

    formatted_combined_total = locale.format_string("%d", combined_total, grouping=True)

    req_MultiConditions_context = required_MultiConditions(request)
    
    current_date = date.today()
    Todays_total_push = Car.objects.filter(entry_time__date=current_date).count()
    Total_push = Car.objects.all().count()

    yesterday = date.today() - timedelta(days=1)
    yesterday_total_push = Car.objects.filter(entry_time__date=yesterday).count()

    push_counts = Car.objects.values('entry_time__date').annotate(push_count=Count('id')).order_by('-entry_time__date')

    all_data = Car.objects.all().order_by('id')

    # Convert queryset to DataFrame
    df = pd.DataFrame(list(push_counts.values('entry_time__date', 'push_count')))

    # Convert 'date' column to datetime
    df['entry_time__date'] = pd.to_datetime(df['entry_time__date']).dt.date

    # Aggregate counts for the same date
    df = df.groupby('entry_time__date').sum().reset_index()

    fig = px.line(df, x='entry_time__date', y='push_count', title='Total Car Push ', markers=True)

    # Convert Plotly figure to JSON string
    line_chart = fig.to_json()

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
        'line_chart': line_chart,
    }
    return render(request, 'analytics.html', context)

@login_required(login_url='login')
def profile(request):
    """
    View for user profile page.

    Args:
        request: HttpRequest object.

    Returns:
        Rendered template for user profile page with context data.
    """
    car_count = Car.objects.filter(user=request.user).count()
    context = {'Car_count': car_count}
    return render(request, 'Auth/profile.html', context)

@login_required(login_url='login')
def history(request):
    """
    View for history page.

    Args:
        request: HttpRequest object.

    Returns:
        Rendered template for history page with context data.
    """
    completedcars = Car.objects.prefetch_related().filter(status='COMPLETED').order_by('-id')

    paginator = Paginator(completedcars, 50)  # 50 records per page
    page_number = request.GET.get('page')

    try:
        completed_cars = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        completed_cars = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        completed_cars = paginator.page(paginator.num_pages)

    total = completedcars.count()

    for car in completed_cars:
        cycle_time = car.exit_time - car.entry_time
        car.cycle_time = format_timedelta(cycle_time)

    context = {
        'Completed': completed_cars,
        'total': total,
    }
    return render(request, 'Datas/history.html', context)

@login_required(login_url='login')
def alldatas(request):
    """
    View for all data page.

    Args:
        request: HttpRequest object.

    Returns:
        Rendered template for all data page with context data.
    """
    request.session['project_name'] = 'example'
    request.session['model_name'] = 'Car'

    alldata = Car.objects.all().select_related('zone', 'Type').order_by('zone')

    paginator = Paginator(alldata, 50)  # 50 records per page
    page_number = request.GET.get('page')

    try:
        all_data = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        all_data = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        all_data = paginator.page(paginator.num_pages)

    total = alldata.count()

    for car in all_data:
        if car.exit_time is not None:
            cycle_time = car.exit_time - car.entry_time
            car.cycle_time = format_timedelta(cycle_time)
        else:
            car.cycle_time = "--"
            
    context = {
        'alldatas': all_data,
        'total': total,
    }
    return render(request, 'Datas/All_records.html', context)

def change_password(request):
    """
    View for changing user password.

    Args:
        request: HttpRequest object.

    Returns:
        Rendered template for changing password page with form data.
    """
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