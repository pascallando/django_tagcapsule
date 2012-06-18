from django import template
from django.utils import simplejson

register = template.Library()

@register.simple_tag
def load_tag_variables(*args, **kwargs):
    values_block = "<!--tagcapsule_values="
    values_block += simplejson.dumps(kwargs)
    values_block += "-->"
    return values_block

    
    