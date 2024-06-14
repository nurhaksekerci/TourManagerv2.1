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



@register.filter
def custom_currency(value):
    if value == 0:
        return '----'
    return f"{value:,.2f}"

@register.filter
def custom_currency_with_unit(value, currency_unit):
    if value == 0:
        return '----'
    return f"{value:,.2f} {currency_unit}"