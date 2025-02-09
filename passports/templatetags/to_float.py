from django import template
from django.template.defaultfilters import floatformat


register = template.Library()


@register.filter
def to_float(value):
    return floatformat(value, arg = 3).replace(',', '.')


@register.filter
def to_float_result(value):
    return floatformat(value, arg = 2).replace(',', '.')