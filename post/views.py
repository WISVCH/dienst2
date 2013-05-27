from django.shortcuts import render_to_response

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

import urls


def index(request):
  return render_to_response('post/dashboard.html', post_data)