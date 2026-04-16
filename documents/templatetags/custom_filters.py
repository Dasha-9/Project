from django import template

register = template.Library()

@register.filter
def split(value, arg):
    """Разделяет строку по разделителю и возвращает список"""
    if not value:
        return []
    return value.split(arg)

@register.filter
def strip(value):
    """Удаляет пробелы в начале и конце строки"""
    if not value:
        return value
    return value.strip()
