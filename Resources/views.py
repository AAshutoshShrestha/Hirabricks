from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Sum
from .forms import BurnerConsumptionForm, JhogaiConsumptionForm
from .models import BurnerConsumption, JhogaiConsumption,METHOD_CHOICES

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


def reports(request):
    burner = BurnerConsumption.objects.all().order_by('burner_number','-date')
    jhogai = JhogaiConsumption.objects.order_by('type')

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
    return render(request, 'reports.html', context)