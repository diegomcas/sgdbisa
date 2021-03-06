"""---"""
from django import template

register = template.Library()


@register.filter(name='addclass')
def addclass(field, arg):
    """---"""
    return field.as_widget(attrs={'class': arg})


@register.filter(name='field_type')
def field_type(field):
    """---"""
    return field.field.widget.__class__.__name__
