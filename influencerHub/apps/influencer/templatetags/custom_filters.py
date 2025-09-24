from django import template

register = template.Library()

@register.filter(name='split')
def split_filter(value, delimiter=','):
    return value.split(delimiter) if value else []
