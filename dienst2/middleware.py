from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.core.urlresolvers import resolve


class RequireLoginMiddleware(object):
    """
    Require Login middleware. If enabled, each Django-powered page will
    require authentication. Also checks API key for requests to API.

    Based on:
    http://djangosnippets.org/snippets/136/
    http://stackoverflow.com/questions/2164069/best-way-to-make-djangos-login-required-the-default
    """

    def __init__(self):
        self.require_login_path = getattr(settings, 'LOGIN_URL', '/accounts/login/')

    def process_request(self, request):
        if request.user.is_authenticated():
            return

        # resolve() will raise an Http404 error if url not found
        r = resolve(request.path_info)

        # django-rest-framework (DEFAULT_PERMISSION_CLASSES in settings.py)
        if r._func_path.startswith("rest_framework.") or r._func_path.startswith("ldb.viewsets."):
            return

        # other pages except login page
        elif request.path != self.require_login_path:
            return redirect_to_login(request.path)
