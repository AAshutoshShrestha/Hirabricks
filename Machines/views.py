from django.shortcuts import render, redirect
from .forms import MachineRuntimeForm
from django.utils import timezone
from datetime import date
from django.contrib.auth.decorators import login_required
from .models import MachineOperator,MachineRuntime

from django.contrib import messages

@login_required
def record_time(request):
    today = date.today()
    user = request.user

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



def runtime_records(request):
    runtime_records  = MachineRuntime.objects.all()
    context = {
        'Runtime_details': runtime_records,
    }
    return render(request, 'Machine/Records.html', context)
