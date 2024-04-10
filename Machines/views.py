from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, F
from datetime import date
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
import requests
from django.views.decorators.csrf import csrf_exempt
from django.db.models.functions import TruncDate
import json 
from .forms import MachineRuntimeForm, MaintenanceTaskForm, MaintenanceUpdateForm
from .models import *

from vercel_app.generategraphs import generate_dryer_efficiency_graph

# Importing environment variables
import os
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Supabase client
url = os.environ.get('SUPABASE_URL')
key = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
supabase = create_client(url, key)

# Firebase Realtime Database URL
FIREBASE_DB_URL = "https://tunnel-kiln-default-rtdb.asia-southeast1.firebasedatabase.app/"

# Function to check machine status
def check_machine_status():
    """
    Check the status of the machine from Firebase Realtime Database.
    """
    response = requests.get(FIREBASE_DB_URL + "/Sensor/Machine_status.json")
    machine_status = response.json()
    if machine_status == 1:
        status = "machine started"
    else:
        status = "machine stopped"
    return status

@csrf_exempt
def machine_status_update(request):
    """
    Update machine status based on the data received from Firebase Realtime Database.
    """
    operator = MachineOperator.objects.first()
    runtime_records = MachineRuntime.objects.filter(start_time__date=date.today(), machine_operator__user=request.user)
    try:
        machine_runtime = MachineRuntime.objects.filter(machine_operator=operator, end_time__isnull=True).latest('start_time')
    except MachineRuntime.DoesNotExist:
        machine_runtime = None

    if request.method == 'GET':
        state = check_machine_status()
        
        if state == "machine started" and (not machine_runtime or machine_runtime.end_time is not None):
            # Machine started and previous state was stopped or no record exists
            machine_runtime = MachineRuntime(start_time=timezone.now(), machine_operator=operator)
            machine_runtime.save()
            messages.success(request, "The machine has started running.")
        
        elif state == "machine stopped" and machine_runtime and machine_runtime.end_time is None:
            # Machine stopped and previous state was started
            machine_runtime.end_time = timezone.now()
            machine_runtime.save()
            messages.success(request, "The machine has stopped running.")
    
    context = {
        'Runtime_details': runtime_records,
    }

    return render(request, 'Machine/Runtime.html', context)

@login_required(login_url='login')
def record_time(request):
    """
    Record the machine runtime.
    """
    today = date.today()
    user = 1

    runtime_records = MachineRuntime.objects.filter(start_time__date=today, machine_operator__user=user)
    operator = MachineOperator.objects.get(user=request.user)
    try:
        machine_runtime = MachineRuntime.objects.filter(machine_operator=operator, end_time__isnull=True).latest('start_time')
    except MachineRuntime.DoesNotExist:
        machine_runtime = None

    form = MachineRuntimeForm()

    if request.method == 'POST':
        if 'start' in request.POST:
            if not machine_runtime:
                form = MachineRuntimeForm(request.POST)
                if form.is_valid():
                    machine_runtime = form.save(commit=False)
                    machine_runtime.start_time = timezone.now()
                    machine_runtime.machine_operator = operator
                    machine_runtime.save()
                    messages.success(request, "The machine has started running.")
            else:
                messages.error(request, "The machine is already in Running state")

        elif 'end' in request.POST:
            if machine_runtime:
                machine_runtime.end_time = timezone.now()
                machine_runtime.save()
                messages.success(request, "The machine has stopped running.")
            else:
                messages.error(request, "The machine is not running yet")

        return redirect('machine_runtime')  # Redirect after setting the message

    context = {
        'Runtime_details': runtime_records,
        'form': form
    }

    return render(request, 'Machine/Runtime.html', context)

@login_required(login_url='login')
def runtime_records(request):
    """
    Display machine runtime records.
    """
    request.session['project_name'] = 'Machines'
    request.session['model_name'] = 'MachineRuntime'
    
    # Retrieve runtime records from the database
    runtime_records = MachineRuntime.objects.order_by('id').all()

    labels = []
    data = []

   # Aggregate work durations for each unique date
    work_durations_by_date = MachineRuntime.objects.values(
        'start_time__date', 'machine_operator__user__username', 'machine_operator__machine__name'
    ).annotate(
        total_duration=Sum(F('end_time') - F('start_time'))
    )

    for query in work_durations_by_date:
        labels.append(query['start_time__date'].strftime('%Y-%m-%d'))
        data.append(query['total_duration'].total_seconds() // 3600)
    # Convert lists to JSON format
    labels_json = json.dumps(labels)
    data_json = json.dumps(data)

    context = {
        'Runtime_details': runtime_records,
        'work_durations_by_date': work_durations_by_date,
        'labels': labels_json,
        'data': data_json,
    }

    # Render the template with the context data
    return render(request, 'Machine/Records.html', context)


@login_required(login_url='login')
def maintenance_tasks(request):
    """
    Manage maintenance tasks.
    """
    form = MaintenanceTaskForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            last_record = MaintenanceTask.objects.last()  # Get the last record
            new_id = last_record.id + 1 if last_record else 1  # Increment the ID
            state = "Pending"

            create = form.save(commit=False)
            create.id = new_id  # Assign the new ID
            create.user = request.user  # Assign the currently logged-in user
            create.date = timezone.now()  # Assign the current date/time
            create.status = state
            create.save()
            messages.success(request, "Maintenance Request Received successfully")
            return redirect('maintenance_tasks')
    
    machinearea = MachineArea.objects.all()
    machines = Machine.objects.all()

    pending_tasks = MaintenanceTask.objects.filter(status='Pending')
    onprocess_tasks = MaintenanceTask.objects.filter(status='Onprocess')
    completed_tasks = MaintenanceTask.objects.filter(status='Completed', date=date.today())
    Onhold_tasks = MaintenanceTask.objects.filter(status='Onhold')

    context ={
        'forms': form, 
        'machinearea': machinearea,
        'machines': machines,
        'pending_tasks': pending_tasks, 
        'onprocess_tasks': onprocess_tasks, 
        'completed_tasks': completed_tasks,
        'Onhold_tasks': Onhold_tasks,
    }
    return render(request, 'Machine/addtask.html', context)

def delete_task(request, pk):
    """
    Delete a maintenance task by id
    """
    obj = get_object_or_404(MaintenanceTask, id=pk)
    
    if request.method == "POST":
        obj.delete()
        return JsonResponse({'message': 'success'}, status=200)
    
    return render(request, "Machine/delete_task.html", {'obj': obj})

@login_required(login_url='login')  
def update_task_status(request, pk):
    """
    Update the status of a maintenance task.
    """
    Maintenance_Task = get_object_or_404(MaintenanceTask, pk=pk)
    if request.method == 'POST':
        form = MaintenanceUpdateForm(request.POST, instance=Maintenance_Task)
        if form.is_valid():
            form.save()
            return redirect('maintenance_tasks')
        
    else:
        form = MaintenanceUpdateForm(instance=Maintenance_Task)

    context = {
        'forms': form,
        'Maintenance_Task': Maintenance_Task,
    }

    return render(request, "Machine/updateTask.html", context)
