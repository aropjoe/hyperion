from django import template

register = template.Library()


@register.filter
def multiply(value):
    return value * 100
