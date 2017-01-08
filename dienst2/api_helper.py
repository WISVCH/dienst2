from __future__ import unicode_literals

from django.conf.urls import url
from django.core.exceptions import ValidationError
from tastypie.authorization import DjangoAuthorization
from tastypie.cache import SimpleCache
from tastypie.utils import trailing_slash
from tastypie.validation import Validation


class CHValidation(Validation):
    def is_valid(self, bundle, request=None):
        try:
            bundle.obj.full_clean()
        except ValidationError as e:
            return e

        return {}


def prepend_urls():
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_search'), name="api_search_" + self._meta.resource_name),
        ]

    return prepend_urls


class BaseMeta:
    authorization = DjangoAuthorization()
    always_return_data = True
    cache = SimpleCache(timeout=10)
    validation = CHValidation()
