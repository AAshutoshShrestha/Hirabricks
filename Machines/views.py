from django.shortcuts import render, redirect
from datetime import date
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
import requests
from django.views.decorators.csrf import csrf_exempt

from .forms import MachineRuntimeForm,MaintenanceTaskForm
from .models import *

import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()


url=os.environ.get('SUPABASE_URL')
key=os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
supabase = create_client(url, key)



# Firebase Realtime Database URL
FIREBASE_DB_URL = "https://tunnel-kiln-default-rtdb.asia-southeast1.firebasedatabase.app/"

# Function to check machine status
def check_machine_status():
    # Get data from Firebase
    response = requests.get(FIREBASE_DB_URL + "/Sensor/Machine_status.json")
    machine_status = response.json()
    if machine_status == 1:
        status = "machine started"
    else:
        status =  "machine stopped"
    return status

@csrf_exempt
def machine_status_update(request):
    runtime_records = MachineRuntime.objects.all()
    operator = MachineOperator.objects.first()
    try:
        machine_runtime = MachineRuntime.objects.filter(machine_operator=operator, end_time__isnull=True).latest('start_time')
    except MachineRuntime.DoesNotExist:
        machine_runtime = None

    if request.method == 'GET':
        state = check_machine_status()
        form = MachineRuntimeForm(request.POST)
        if state == "machine started":
                machine_runtime = form.save(commit=False)
                machine_runtime.start_time = timezone.now()
                machine_runtime.machine_operator = operator
                machine_runtime.save()

                messages.success(request, "The machine has started running.")

            # Code to save start_time to Supabase
        elif state == "machine stopped":
            if machine_runtime:
                machine_runtime.end_time = timezone.now()
                machine_runtime.save()
                messages.success(request, "The machine has stopped running.")
            
    context = {
        'Runtime_details': runtime_records,
   
    }

    return render(request, 'Machine/Runtime.html', context)


@login_required(login_url='login')
def record_time(request):
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
    request.session['project_name'] = 'Machines'
    request.session['model_name'] = 'MachineRuntime'
    
    # Retrieve runtime records from the database
    runtime_records = MachineRuntime.objects.all()
    
    # Pass the plot_div to the template context
    context = {
        'Runtime_details': runtime_records,
    }
    # Render the template with the context data
    return render(request, 'Machine/Records.html', context)

@login_required(login_url='login')
def maintenance_tasks(request):
    form =MaintenanceTaskForm()
    pending_tasks = MaintenanceTask.objects.filter(status='Pending')
    onprocess_tasks = MaintenanceTask.objects.filter(status='Onprocess')
    completed_tasks = MaintenanceTask.objects.filter(status='Completed')
    Onhold_tasks = MaintenanceTask.objects.filter(status='Onhold')
    context ={
        'forms': form, 
        'pending_tasks': pending_tasks, 
        'onprocess_tasks': onprocess_tasks, 
        'completed_tasks': completed_tasks,
        'Onhold_tasks': Onhold_tasks
    }
    return render(request, 'drag&drop.html', context)

@login_required(login_url='login')
def update_task_status(request, task_id):
    if request.method == 'POST' and request.is_ajax():
        new_status = request.POST.get('new_status')
        try:
            task = MaintenanceTask.objects.get(pk=task_id)
            task.status = new_status
            task.save()
            return JsonResponse({'success': True})
        except MaintenanceTask.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Task does not exist'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})
