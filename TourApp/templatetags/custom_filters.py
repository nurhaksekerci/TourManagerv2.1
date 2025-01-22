from django import template

register = template.Library()

@register.filter
def get_field_value(obj_data, field_name):
    if isinstance(obj_data, dict):
        # Eğer field_name bir liste ise, her bir eleman için değeri döndürün.
        if isinstance(field_name, list):
            return [obj_data.get(field, '') for field in field_name]
        # Eğer field_name bir string ise, tek bir değeri döndürün.
        elif field_name in obj_data:
            return obj_data[field_name]
    elif isinstance(obj_data, list):
        # Eğer obj_data bir liste ise, field_name içindeki verileri döndürmek için ilk elemanı kullanın.
        if obj_data and isinstance(obj_data[0], dict):
            return obj_data[0].get(field_name, '')
    return ''
