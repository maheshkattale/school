# templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter(name='startswith')
def startswith(value, arg):
    return value.startswith(arg)
