import urllib.parse

from django.contrib.auth import (
    SESSION_KEY,
    _get_user_session_key,
    get_backends,
    login,
    logout,
)
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import resolve, reverse
from django.utils.deprecation import MiddlewareMixin

from dienst2 import settings
from dienst2.auth import IAPBackend


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
            or r._func_path.startswith("rest_framework.")
            or r._func_path.startswith("ldb.viewsets.")
            or r.url_name == "forbidden"
        ):
            return

        if request.user.is_authenticated:
            if not IAPBackend.can_authenticate(request):
                logout(request)
        elif settings.DANGEROUSLY_ALLOW_AUTOLOGIN:
            # DEBUG: Automatically log in as admin
            # Create admin user if it doesn't exist
            if not User.objects.filter(username="admin").exists():
                user = User.objects.create(
                    username="admin",
                    is_active=True,
                    is_staff=True,
                    is_superuser=True,
                    is_admin=True,
                )

            else:
                user = User.objects.get(username="admin")
            login(request, user)
            return

        else:
            backends = get_backends()
            try:
                iap_backend = next(
                    filter(lambda be: isinstance(be, IAPBackend), backends)
                )
            except StopIteration:
                iap_backend = None

            # Try to authenticate with IAP if the headers
            # are available
            if iap_backend and IAPBackend.can_authenticate(request):
                # Calling login() cycles the csrf token which causes POST request
                # to break. We only call login if authenticating with IAP changed
                # the user ID in the session, or the user ID was not in the session
                # at all.
                user = iap_backend.authenticate(request)
                if user and user.is_authenticated:
                    should_login = (
                        SESSION_KEY not in request.session
                        or _get_user_session_key(request) != user.pk
                    )

                    if should_login:
                        # Setting the backend is needed for the call to login
                        login(request, user)
                    else:
                        # If we don't call login, we need to set request.user ourselves
                        # and update the backend string in the session
                        request.user = user

                    return

        # Forbidden
        return redirect(
            "{}?next={}".format(reverse("forbidden"), urllib.parse.quote(request.path))
        )
