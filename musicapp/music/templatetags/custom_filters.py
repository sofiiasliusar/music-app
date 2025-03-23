#TODO
from django import template
from datetime import timedelta

register = template.Library()

@register.filter
def format_duration(value):
    if isinstance(value, timedelta):
        minutes = value.seconds // 60
        seconds = value.seconds % 60
        return f"{minutes:02}:{seconds:02}"
    return value
