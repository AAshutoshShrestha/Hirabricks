from django import template
import locale

register = template.Library()

# Set the locale to the user's default setting
locale.setlocale(locale.LC_ALL, '')

@register.filter(name='convert')
def convert_to_hours_and_minutes(value):
    try:
        value = int(value)  # Convert value to integer
        hours = value // 60
        minutes = value % 60
        return f"{hours} hours {minutes} minutes"
    except (TypeError, ValueError):
        return "Invalid input"



@register.filter(name='multiply')
def multiply(value, arg):
    # Check if value is None
    if value is None:
        return "--"

    total = value * arg
    formatted_total = locale.format_string("%d", total, grouping=True)
    return formatted_total