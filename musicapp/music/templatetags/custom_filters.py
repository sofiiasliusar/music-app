#TODO
from django import template
from datetime import timedelta

register = template.Library()

@register.filter
def format_duration(value):
    if isinstance(value, timedelta):
        total_seconds = int(value.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        if hours > 0:
            return f"{hours}:{minutes:02}:{seconds:02}"  # Include hours
        return f"{minutes}:{seconds:02}"
    return value
