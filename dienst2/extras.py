from django.db import models


class CharNullField(models.CharField):  # subclass the CharField
    description = "CharField that stores NULL but returns ''"
    __metaclass__ = models.SubfieldBase  # this ensures to_python will be called

    def to_python(self, value):
        # this is the value right out of the db, or an instance
        # if an instance, just return the instance
        if isinstance(value, models.CharField):
            return value
        if value is None:  # if the db has a NULL (None in Python)
            return ''  # convert it into an empty string
        else:
            return value  # otherwise, just return the value

    def get_prep_value(self, value):  # catches value right before sending to db
        if value is None or value.strip() == '':
            # if Django tries to save an empty string, send the db None (NULL)
            return None
        else:
            # otherwise, just pass the value
            return value


SEARCH_FORMATS = {
    'default': '*{}*',
    'start': '{}*',
    'exact': '{}',
}


def convert_free_search(string, mod='default'):
    search_format = SEARCH_FORMATS[mod]
    return ' '.join([search_format.format(word) for word in string.split(' ')])
