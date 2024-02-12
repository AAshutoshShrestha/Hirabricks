from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *

from examples.models import Car, Firing


@login_required(login_url='login')
def required_conditions(request):
    Firing = Firing.objects.filter(id=1)
    context={
        'Firing': Firing, 
    }
    return context