from django import template

register = template.Library()


@register.filter
def get_attr(obj, attr_name):
    """
    Obtiene un atributo de un objeto dinámicamente.
    Soporta notación con puntos para atributos anidados: "fk_lugar.nombre"
    Soporta métodos sin argumentos: "get_estado_display"
    """
    if not attr_name:
        return obj

    parts = attr_name.split('.')
    value = obj

    for part in parts:
        if value is None:
            return None

        # Intentar como atributo
        if hasattr(value, part):
            attr = getattr(value, part)
            # Si es callable (método), ejecutarlo
            if callable(attr):
                value = attr()
            else:
                value = attr
        # Intentar como clave de diccionario
        elif isinstance(value, dict) and part in value:
            value = value[part]
        else:
            return None

    return value


@register.filter
def get_item(dictionary, key):
    """
    Obtiene un valor de un diccionario por clave.
    Uso: {{ my_dict|get_item:key }}
    """
    if dictionary is None:
        return None
    return dictionary.get(key)


@register.simple_tag
def url_with_params(url_name, pk=None, **kwargs):
    """
    Genera URL con parámetros adicionales.
    """
    from django.urls import reverse
    if pk:
        url = reverse(url_name, args=[pk])
    else:
        url = reverse(url_name)

    if kwargs:
        params = '&'.join(f'{k}={v}' for k, v in kwargs.items() if v)
        if params:
            url = f'{url}?{params}'

    return url
