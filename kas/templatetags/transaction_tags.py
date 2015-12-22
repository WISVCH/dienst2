from django import template
from django.template.defaultfilters import floatformat
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()


@register.filter
def is_valid(transaction):
    return transaction.valid


@register.filter
def currency(amount):
    return u"\u20AC %s" % intcomma(floatformat(amount, 2))
