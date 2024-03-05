import tempfile
from django.http import JsonResponse

from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Sum
from .forms import BurnerConsumptionForm, JhogaiConsumptionForm, MixtureForm
from .models import *
from datetime import timedelta,date

def coals(request):
    burner_form = BurnerConsumptionForm(request.POST)
    jhogai_form = JhogaiConsumptionForm(request.POST)
    if request.method == 'POST':
        if burner_form.is_valid():
            by = request.user
            coalweight = request.POST.get('coal_weight')
            burnernumber = request.POST.get('burner_number')
            Bform = BurnerConsumption.objects.create(
                user=by,    
                date=timezone.now(),
                coal_weight=coalweight,
                burner_number=burnernumber,
            )
            Bform.save()
            return redirect('resource_form')
    if request.method == 'POST':    
        if jhogai_form.is_valid(): 
            by = request.user
            type = request.POST.get('type')
            weight = request.POST.get('weight')

            jform = JhogaiConsumption.objects.create(
                user=by,
                date=timezone.now(),
                type=type,
                weight=weight,
            )
            jform.save()
            return redirect('resource_form')

    burner_form = BurnerConsumptionForm()
    jhogai_form = JhogaiConsumptionForm()
    
    context = {
        'Burnerform': burner_form,
        'Jhogaiform': jhogai_form
    }
    return render(request, 'coals.html', context)

def todaysRecord(request):
    Today = date.today()
    
    # Filter BurnerConsumption records by Today's date
    burner = BurnerConsumption.objects.filter(date__date=Today).order_by('burner_number')
    
    # Check if burner content is empty
    burner_empty = not burner.exists()

    # Filter JhogaiConsumption records by Today's date
    jhogai = JhogaiConsumption.objects.filter(date__date=Today).order_by('type')

    jhogai_types = [choice[0] for choice in METHOD_CHOICES]
    jhogai_totals = {}

    for type_value in jhogai_types:
        # Calculate total sum of weight for each type for Today's date
        total_weight = JhogaiConsumption.objects.filter(date__date=Today, type=type_value).aggregate(total_weight=Sum('weight'))['total_weight'] or 0
        jhogai_totals[type_value] = total_weight

    # Create a list of dictionaries containing type and corresponding total weight
    jhogai_totals_list = [{'type': type_value, 'total_weight': jhogai_totals.get(type_value, 0)} for type_value in jhogai_types]

    # Calculate total sum of coal_weight for Today's date
    burner_total_weight = BurnerConsumption.objects.filter(date__date=Today).aggregate(total_weight=Sum('coal_weight'))['total_weight'] or 0
    
    context = {
        'METHOD_CHOICES': METHOD_CHOICES,
        'Burner': burner,
        'Jhogai': jhogai,
        'burner_total_weight': burner_total_weight,
        'jhogai_totals_list': jhogai_totals_list,
        'burner_empty': burner_empty,
    }
    return render(request, 'todays_coal_report.html', context)


def reports(request):
    burner = BurnerConsumption.objects.all().order_by('burner_number','-date')
    jhogai = JhogaiConsumption.objects.all().order_by('type')

    jhogai_types = [choice[0] for choice in METHOD_CHOICES]
    jhogai_totals = {}

    for type_value in jhogai_types:
        # Calculate total sum of weight for each type
        total_weight = JhogaiConsumption.objects.filter(type=type_value).aggregate(total_weight=Sum('weight'))['total_weight'] or 0
        jhogai_totals[type_value] = total_weight

    # Create a list of dictionaries containing type and corresponding total weight
    jhogai_totals_list = [{'type': type_value, 'total_weight': jhogai_totals.get(type_value, 0)} for type_value in jhogai_types]

    # Calculate total sum of coal_weight
    burner_total_weight = BurnerConsumption.objects.aggregate(total_weight=Sum('coal_weight'))['total_weight'] or 0
    

    context = {
        'METHOD_CHOICES': METHOD_CHOICES,
        'Burner': burner,
        'Jhogai': jhogai,
        'burner_total_weight': burner_total_weight,
        'jhogai_totals_list': jhogai_totals_list,
        
    }
    return render(request, 'All_coal_records.html', context)

def soil_mixture(request):
    if request.method == 'POST':
        formset = MixtureForm(request.POST, request.FILES)
        if formset.is_valid():
            # Extract data from the form
            type = request.POST.get('type')
            sand = request.POST.get('sand')
            silt = request.POST.get('silt')
            clay = request.POST.get('clay')
            remarks = request.POST.get('remarks')
            soilimg = request.FILES.get('soil_img')

            by=request.user
            # Create a new Mixture instance
            mix = SoilDetails.objects.create(
                user=by,
                date=timezone.now() ,
                type=type,
                sand=sand,
                silt=silt,
                clay=clay,
                remarks=remarks,
                soil_img=soilimg,
            )
            # Save the Mixture instance
            mix.save()
            return redirect('soil_mixture')
    else:
        formset = MixtureForm()
    context = {
        'formset': formset,
    }
    return render(request, 'soil.html', context)
