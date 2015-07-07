from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from django.utils.translation import ugettext as _
from django import forms
from django.utils.datastructures import SortedDict
import copy

register = template.Library()

@register.filter
def janee(value):
    if value:
    	return 'Ja'
    else:
    	return 'Nee'

@register.inclusion_tag('ldb/trow.html')
def trow(o, k):
    return {'key': _(capfirst(o._meta.get_field(k).verbose_name)), 'value': getattr(o, k)}

@register.inclusion_tag('ldb/stcontrol.html')
def stcontrol(o, k):
    return {'key': _(capfirst(o._meta.get_field(k).verbose_name)), 'value': getattr(o, k)}

@register.inclusion_tag('ldb/stcontrol.html')
def stcontrol_janee(o, k):
    return {'key': _(capfirst(o._meta.get_field(k).verbose_name)), 'value': janee(getattr(o, k))}

@register.inclusion_tag('ldb/stcontrol.html')
def stcontrol_format(o, k, format):
    return {'key': _(capfirst(o._meta.get_field(k).verbose_name)), 'value': mark_safe(format.format(getattr(o, k))), 'empty':getattr(o, k)==''}

@register.inclusion_tag('ldb/trow.html')
def trow_janee(o, k):
    return {'key': _(capfirst(o._meta.get_field(k).verbose_name)), 'value': janee(getattr(o, k))}

@register.tag
def get_fieldset(parser, token):
    try:
        name, fields, as_, variable_name, from_, form = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('bad arguments for %r'  % token.split_contents()[0])

    return FieldSetNode(fields.split(','), variable_name, form)

class FieldSetNode(template.Node):
    def __init__(self, fields, variable_name, form_variable):
        self.fields = fields
        self.variable_name = variable_name
        self.form_variable = form_variable

    def render(self, context):
        form = template.Variable(self.form_variable).resolve(context)
        new_form = copy.copy(form)        
        new_form.fields = SortedDict([(key, value) for key, value in form.fields.items() if key in self.fields])

        context[self.variable_name] = new_form

        return u''
