from django import template

register = template.Library()

@register.filter
def convert_to_hours_and_minutes(value):
    hours = value // 60
    minutes = value % 60
    return f"{hours} hours, {minutes} minutes"