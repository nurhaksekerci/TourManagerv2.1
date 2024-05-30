from django import template

register = template.Library()

@register.filter
def get_field_value(obj_data, field_name):
    return obj_data[field_name]

@register.filter
def currency(value):
    try:
        value = float(value)
        return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except ValueError:
        return value