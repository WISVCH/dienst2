from django.conf import settings
from django.core.urlresolvers import resolve
from django.http import HttpResponse
from django.shortcuts import redirect
from tastypie import http
from tastypie.authentication import ApiKeyAuthentication


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
        view_name = resolve(request.path).view_name
        if view_name.startswith('api_'):
            auth = ApiKeyAuthentication()
            auth_result = auth.is_authenticated(request)

            if isinstance(auth_result, HttpResponse):
                return auth_result

            if auth_result is not True:
                return http.HttpUnauthorized()

        elif request.path != self.require_login_path:
            return redirect('%s?next=%s' % (self.require_login_path, request.path))
