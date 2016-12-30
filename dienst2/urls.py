from django.conf.urls import include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.defaults import page_not_found
from django.views.defaults import server_error

from dienst2 import settings
from dienst2.views import index

admin.autodiscover()

urlpatterns = [
    # The LDB index:
    url(r'^$', index, name='index'),

    # The Admin docs:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # The Admin site:
    url(r'^admin/', include(admin.site.urls)),

    # The signin page
    url(r'^accounts/login/$', auth_views.login, name='login'),

    # The logout page
    url(r'^accounts/logout/$', auth_views.logout, name='logout'),

    # LDB URLs
    url(r'^ldb/', include('ldb.urls')),

    # Post URLs
    url(r'^post/', include('post.urls')),

    # Post URLs
    url(r'^kas/', include('kas.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^404/$', page_not_found),
        url(r'^500/$', server_error),
    ]
