from django.conf.urls import patterns, url, include
from tastypie.api import Api

from post.api import *


api = Api(api_name='v2')
api.register(CategoryResource())
api.register(SourceResource())
api.register(ItemResource())

urlpatterns = patterns('',
                       (r'^api/', include(api.urls)),

                       url(r'^$', 'post.views.index', name="post_index"),
)
