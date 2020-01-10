from django.db import models


class MembershipStatusField(models.IntegerField):
    def __init__(self, enum, *args, **kwargs):
        self.enum = enum
        kwargs['choices'] = self.enum.choices()
        super(MembershipStatusField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(
            MembershipStatusField, self).deconstruct()
        if self.enum is not None:
            kwargs['enum'] = self.enum
        if 'choices' in kwargs:
            del kwargs['choices']
        return name, path, args, kwargs

