import datetime

from django import template
from django.utils import formats
from django.utils.encoding import force_str

register = template.Library()


@register.simple_tag(takes_context=True)
def group_by_description(context, items):
    filter = context.get('filter')

    if filter is not None:
        value = filter.data.get('date', None)
        date = None
        for format in formats.get_format('DATE_INPUT_FORMATS'):
            try:
                date = datetime.datetime.strptime(force_str(value), format).date()
            except (ValueError, TypeError):
                continue
        if date is not None:
            items = items.filter(date__gte=date)
    return items.group_by_description()


@register.filter()
def strftime(date, format):
    return date.strftime(format)
