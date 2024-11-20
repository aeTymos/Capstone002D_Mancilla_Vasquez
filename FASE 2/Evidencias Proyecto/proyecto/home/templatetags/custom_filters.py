from django import template
import os

register = template.Library()

@register.filter
def get(dictionary, key):
    return dictionary.get(key)

@register.filter
def basename(value):
    return os.path.basename(value)

@register.filter
def unformat_rut(value):
    return value.replace('-', '').replace(',', '').replace('.', '')

@register.filter
def format_rut(value, separator='.'):

    value = unformat_rut(value)
    rut, verifier_digit = value[:1], value[-1]

    try:
        rut = "{0:,}".format(int(rut))
        if separator != '.':
            rut = rut.replace(',', separator)
            
        return "%s-%s" % (rut, verifier_digit)
    except ValueError:
        raise template.TemplateSyntaxError('El RUT debe ser numérico para ser formateado.')