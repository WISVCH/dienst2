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


def get_search(Model):
    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        # Do the query.
        q = request.GET.get('q', '')
        mod = request.GET.get('mod', 'default')
        sqs = SearchQuerySet().models(Model).load_all().filter(text=Raw(convert_free_search(q, mod)))
        sqs = filter(None, sqs)
        paginator = Paginator(sqs, 20)

        try:
            page = paginator.page(int(request.GET.get('page', 1)))
        except InvalidPage:
            raise Http404("Sorry, no results on that page.")

        objects = []

        for result in page.object_list:
            bundle = self.build_bundle(obj=result.object, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)

        object_list = {
            'objects': objects,
            'meta': {'total_count': len(sqs)}
        }

        self.log_throttled_access(request)
        return self.create_response(request, object_list)

    return get_search


class BaseMeta:
    authorization = DjangoAuthorization()
    always_return_data = True
    cache = SimpleCache(timeout=10)
    validation = CHValidation()
