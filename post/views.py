from django.shortcuts import render_to_response
from django.template import RequestContext

post_data = {
    'title': 'Post',
    'ng_app': 'post',
    'navbar': {
        'title': 'Post',
        'items': [
            ('#/dashboard', 'Dashboard'),
            ('#/week', 'Weekoverzicht'),
            ('#/av', 'AV-Overzicht'),
        ]
    }
}


def index(request):
    return render_to_response('post/dashboard.html', post_data, context_instance=RequestContext(request))
