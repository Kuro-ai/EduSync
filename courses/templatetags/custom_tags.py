from django import template
import os

register = template.Library()

@register.filter
def dict_get(d, key):
    try:
        return d.get(key)
    except (AttributeError, TypeError):
        return None

@register.filter(name='get_item')
def get_item(d, key):
    return dict_get(d, key)

@register.filter
def basename(value):
    return os.path.basename(value)
