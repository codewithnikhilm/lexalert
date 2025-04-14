from django import template

register = template.Library()

@register.filter
def get_range(end, start=0):
    return range(start, end + 1)
