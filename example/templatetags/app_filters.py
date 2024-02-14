from django import template

register = template.Library()

@register.filter(name='convert_to_hours_and_minutes')
def convert_to_hours_and_minutes(value):
    try:
        value = int(value)  # Convert value to integer
        hours = value // 60
        minutes = value % 60
        return f"{hours} hours {minutes} minutes"
    except (TypeError, ValueError):
        return "Invalid input"
