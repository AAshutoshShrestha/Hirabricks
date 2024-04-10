import json
from datetime import date
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Sum

from .forms import *
from .models import *

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

@login_required(login_url='login')
def coals(request):
    """
    View for recording coal consumption.

    Args:
        request: HttpRequest object.

    Returns:
        Rendered template for coal consumption form with context data.
    """
    burner_form = BurnerConsumptionForm(request.POST)
    jhogai_form = JhogaiConsumptionForm(request.POST)
    if request.method == 'POST':
        if burner_form.is_valid():
            # Save data for burner consumption
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
            # Save data for jhogai consumption
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
    return render(request, 'Coals/Forms.html', context)

@login_required(login_url='login')
def todaysRecord(request):
    """
    View for displaying today's records.

    Args:
        request: HttpRequest object.

    Returns:
        Rendered template for displaying today's records with context data.
    """
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
    return render(request, 'Coals/Todays.html', context)

@login_required(login_url='login')
def reports(request):
    """
    View for generating reports.

    Args:
        request: HttpRequest object.

    Returns:
        Rendered template for reports with context data.
    """
    request.session['project_name'] = 'Resources'
    request.session['model_name'] = 'BurnerConsumption'

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
    return render(request, 'Coals/Reports.html', context)

@login_required(login_url='login')
def soil_mixture(request):
    """
    View for recording soil mixture details.

    Args:
        request: HttpRequest object.

    Returns:
        Rendered template for soil mixture form with context data.
    """
    if request.method == 'POST':
        formset = MixtureForm(request.POST, request.FILES)
        if formset.is_valid():
            # Extract data from the form
            s_type = request.POST.get('type')
            came_from = request.POST.get('Source')
            sand = request.POST.get('sand')
            silt = request.POST.get('silt')
            clay = request.POST.get('clay')
            remarks = request.POST.get('remarks')
            soilimg = request.FILES.get('soil_img')
            soiltest = request.FILES.get('soil_test_report')

            if came_from == 'other_source':
                source = request.POST.get('other_source')
            else:
                source = came_from
            by = request.user
            # Create a new Mixture instance
            mix = SoilDetails.objects.create(
                user=by,
                date=timezone.now(),
                type=s_type,
                Source=source,
                sand=sand,
                silt=silt,
                clay=clay,
                remarks=remarks,
                soil_img= soilimg.name if soilimg else "None",  # Save the file name in the database
                soil_test_report=soiltest.name if soiltest else "None",  # Save the file name in the database
            )
            # Save the Mixture instance
            mix.save()
            
            # Upload soilimg to Supabase storage
            if soilimg:
                supabase.storage.from_('image-bucket/').upload(soilimg.name, soilimg.read(), {'content-type': 'image/jpeg'})
            # Upload soilimg to Supabase storage bucket named 'image-bucket'
            if soiltest:
                supabase.storage.from_('image-bucket/Reports').upload(soiltest.name, soiltest.read(), {'content-type': 'image/jpeg'})
            return redirect('soil_mixture')
        
    else:
        formset = MixtureForm()
    context = {
        'formset': formset,
    }
    return render(request, 'Soils/Form.html', context)

@login_required(login_url='login')
def Soilreports(request):
    """
    View for generating soil reports.

    Args:
        request: HttpRequest object.

    Returns:
        Rendered template for soil reports with context data.
    """
    request.session['project_name'] = 'Resources'
    request.session['model_name'] = 'SoilDetails'
    soil = SoilDetails.objects.all()
    for soil_detail in soil:
        # Get public URL for soil_img
        res1 = supabase.storage.from_('image-bucket/').get_public_url(soil_detail.soil_img)
        res2 = supabase.storage.from_('image-bucket/Reports/').get_public_url(soil_detail.soil_test_report)
        # Update soil_img field with the public URL
        soil_detail.soil_img = res1
        soil_detail.soil_test_report = res2

    context = {
        'soil_details': soil,
    }
    return render(request, 'Soils/Reports.html', context)


@login_required(login_url='login')
def Dried_record_Form(request):
    """
    View for recording dryer efficiency.

    Args:
        request: HttpRequest object.

    Returns:
        Rendered template for dryer efficiency form with context data.
    """
    if request.method == 'POST':    
        Reportform = Form_Dryer_Efficiency(request.POST)
        if Reportform.is_valid(): 
            last_record = Dryer_Efficiency.objects.last()  # Get the last record
            new_id = last_record.id + 1 if last_record else 1  # Increment the ID

            rep_form = Reportform.save(commit=False)
            rep_form.id = new_id  # Assign the new ID
            rep_form.user = request.user  # Assign the currently logged-in user
            rep_form.date = timezone.now()  # Assign the current date/time

            rep_form.save()
            messages.success(request, "Dryer Record added successfully")

            return redirect('Dryer_Form')
    else:
        Reportform = Form_Dryer_Efficiency()
    
    
    
    context = {
        'dryer_record_form': Reportform,
        
    }
    return render(request, 'Dryer/Dryer_form.html', context)


@login_required(login_url='login')
def DriedBricksReport(request):
    """
    View for generating dried bricks reports.

    Args:
        request: HttpRequest object.

    Returns:
        Rendered template for dried bricks reports with context data.
    """
    # Fetch all Dryer Efficiency data from the database
    dryer_data = Dryer_Efficiency.objects.all().order_by('id')

    # Initialize dictionary to aggregate counts for the same date
    date_count_dict = {}

    # Aggregate counts for the same date
    for entry in dryer_data:
        # Extract date and count from each entry
        date = entry.date.strftime('%B %d, %Y')
        count = entry.Count
        user = entry.user

        # Increment count for the corresponding date
        if date in date_count_dict:
            date_count_dict[date] += count
        else:
            date_count_dict[date] = count

    # Convert aggregated data to list of dictionaries for Plotly
    aggregated_data = [{'date': date, 'count': count,'user':user} for date, count in date_count_dict.items()]

    labels = []
    data = []
    for query in aggregated_data:
        labels.append(query['date'])
        data.append(query['count'])

    # Convert lists to JSON format
    labels_json = json.dumps(labels)
    data_json = json.dumps(data)

    context = {
        'aggregated_data': aggregated_data,  # Pass the aggregated data to the template
        'labels': labels_json,
        'data': data_json,
    }

    return render(request, 'Dryer/records.html', context)

