#TODO
from django import template
from datetime import timedelta

register = template.Library()

@register.filter
def format_duration(value):
    if isinstance(value, timedelta):
        hours = value.seconds // 3600
        minutes = value.seconds // 60
        seconds = value.seconds % 60
        if hours > 0:
            return f"{hours}:{minutes:02}:{seconds:02}"  # Include hours
        return f"{minutes:02}:{seconds:02}"
    return value
