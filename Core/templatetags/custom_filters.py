from django import template

register = template.Library()

@register.filter
def get_field_value(obj_data, field_name):
    return obj_data[field_name]
