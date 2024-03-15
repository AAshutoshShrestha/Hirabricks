import markdown as md
from django import template

from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='markdown')
@stringfilter
def markdown(value):
    try:
        return md.markdown(value, extensions=["markdown.extensions.fenced_code"])
    except (TypeError, ValueError):
        return "Invalid input"