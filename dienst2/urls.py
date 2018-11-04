from django.urls import include, path
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.defaults import page_not_found
from django.views.defaults import server_error

from dienst2 import settings
from dienst2.views import DashboardView

admin.autodiscover()

urlpatterns = [
    # The LDB index:
    path('', DashboardView.as_view(), name='index'),

    # The Admin docs:
    path('admin/doc/', include('django.contrib.admindocs.urls')),

    # The Admin site:
    path('admin/', admin.site.urls),

    # The signin page
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),

    # The logout page
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

    # LDB URLs
    path('ldb/', include('ldb.urls')),

    # Post URLs
    path('post/', include('post.urls')),

    # Post URLs
    path('kas/', include('kas.urls')),

    # Health check
    path('healthz', include('health_check.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),

        path('404/', page_not_found),
        path('500/', server_error),
    ]
