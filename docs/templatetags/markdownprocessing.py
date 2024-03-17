import markdown as md
from django import template

from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='markdown')
@stringfilter
def markdown(value):
    try:
        return md.markdown(value, extensions = [
    'fenced_code',
    'footnotes',
    'attr_list',
    'def_list',
    'tables',
    'abbr',
    'md_in_html'
]
)
    except (TypeError, ValueError):
        return "Invalid input"