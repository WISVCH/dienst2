from django.utils.translation import gettext as _


class MembershipStatus(object):
    NONE = 0
    DONATING = 10
    ALUMNUS = 20
    REGULAR = 30
    ASSOCIATE = 40
    MERIT = 50
    HONORARY = 60

    labels = {
        NONE: _('Not a member'),
        DONATING: _('Donating member'),
        ALUMNUS: _('Alumnus member'),
        REGULAR: _('Regular member'),
        ASSOCIATE: _('Associate member'),
        MERIT: _('Merit member'),
        HONORARY: _('Honorary member'),
    }

    @classmethod
    def choices(cls):
        return [(value, label) for value, label in cls.labels.items()]
