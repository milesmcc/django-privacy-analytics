from django import template

register = template.Library()

@register.filter(name='percent')
def percent(value, arg=2):
    return format(value, f'.2%')