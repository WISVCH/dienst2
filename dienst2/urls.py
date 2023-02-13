# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.urls import include, path
from django.views.defaults import page_not_found, server_error
from django.views.generic.base import TemplateView

from dienst2 import settings
from dienst2.views import DashboardView

admin.autodiscover()

urlpatterns = [
    # The LDB index:
    path("", DashboardView.as_view(), name="index"),
    # The Admin docs:
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    # The Admin site:
    path("admin/", admin.site.urls),
    # OIDC
    path("oidc/", include("mozilla_django_oidc.urls")),
    path("forbidden", TemplateView.as_view(template_name="403.html"), name="forbidden"),
    # LDB URLs
    path("ldb/", include("ldb.urls")),
    # Post URLs
    path("post/", include("post.urls")),
    # Health check
    path("healthz", include("health_check.urls"))
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
        path("404/", page_not_found),
        path("500/", server_error),
    ]
