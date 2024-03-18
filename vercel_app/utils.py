import csv
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.apps import apps
from django.core.serializers import serialize


def download_csv(request, queryset, model_name):
    if not request.user.is_staff:
        raise PermissionDenied

    model = queryset.model
    model_fields = model._meta.fields + model._meta.many_to_many
    field_names = [field.name for field in model_fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{model_name}.csv"'  # Corrected line

    # the csv writer
    writer = csv.writer(response)
    # Write a first row with header information
    writer.writerow(field_names)
    # Write data rows
    for row in queryset:
        values = []
        for field in field_names:
            value = getattr(row, field)
            if callable(value):
                try:
                    value = value() or ''
                except:
                    value = 'Error retrieving value'
            if value is None:
                value = ''
            values.append(value)
        writer.writerow(values)
    return response


def export_csv(request):
    project_name = request.session.get('project_name', '')
    model_name = request.session.get('model_name', '')
    # Get the app config for the provided project name
    app_config = apps.get_app_config(project_name)

    # Get the model class dynamically using the provided model name
    model = app_config.get_model(model_name)

    queryset = model.objects.all()
    
    data = download_csv(request, queryset, model_name)  # Pass model_name to the function
    return data  # Just returning the HttpResponse object is enough for download