#Medical\templatetags\form_filters.py
from django import template
from django.forms.boundfield import BoundField

register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    if isinstance(value, BoundField):
        css_classes = value.field.widget.attrs.get('class', '')
        if css_classes:
            css_classes = f"{css_classes} {arg}"
        else:
            css_classes = arg
        return value.as_widget(attrs={'class': css_classes})
    return value

@register.filter(name='attr')
def attr(value, arg):
    if isinstance(value, BoundField):
        attrs = dict(x.split(':') for x in arg.split('|'))
        value.field.widget.attrs.update(attrs)
        return value
    return value 




