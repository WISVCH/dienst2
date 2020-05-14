import urllib.parse

from django.shortcuts import redirect
from django.urls import resolve, reverse
from django.utils.deprecation import MiddlewareMixin


class RequireLoginMiddleware(MiddlewareMixin):
    """
    Require Login middleware. If enabled, each Django-powered page will
    require authentication. Also checks API key for requests to API.

    Based on:
    http://djangosnippets.org/snippets/136/
    http://stackoverflow.com/questions/2164069/best-way-to-make-djangos-login-required-the-default
    """

    def __init__(self, get_response=None):
        super().__init__(get_response)

    def process_request(self, request):
        if request.user.is_authenticated:
            return

        # resolve() will raise an Http404 error if url not found
        r = resolve(request.path_info)

        # django-rest-framework (DEFAULT_PERMISSION_CLASSES in settings.py)
        if (
            r._func_path.startswith("health_check.")
            or r._func_path.startswith("mozilla_django_oidc.")
            or r._func_path.startswith("rest_framework.")
            or r._func_path.startswith("ldb.viewsets.")
            or r.url_name == "forbidden"
        ):
            return

        # other pages except login page
        return redirect(
            reverse("oidc_authentication_init")
            + "?next="
            + urllib.parse.quote_plus(request.path)
        )
