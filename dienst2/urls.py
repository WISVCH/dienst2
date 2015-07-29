from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from dienst2 import settings

admin.autodiscover()

urlpatterns = patterns('',
                       # The LDB index:
                       url(r'^$', 'dienst2.views.index', name='index'),

                       # The Admin docs:
                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # The Admin site:
                       url(r'^admin/', include(admin.site.urls)),

                       # The signin page
                       url(r'^accounts/login/$', 'django.contrib.auth.views.login'),

                       # LDB URLs
                       url(r'^ldb/', include('ldb.urls')),

                       # Post URLs
                       url(r'^post/', include('post.urls')),

                       # Post URLs
                       url(r'^kas/', include('kas.urls')),
                       )

if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^404/$', 'django.views.defaults.page_not_found'),
                            (r'^500/$', 'django.views.defaults.server_error'),
                            )
