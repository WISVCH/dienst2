from django.shortcuts import render_to_response

post_data = {
  'title': 'Ledendatabase', 
  'ng_app': 'ldb',
  'navbar': {
    'title': 'Ledendatabase',
    'items': [
      ('#/dashboard', 'Dashboard'),
    ]
  }
}

import urls

def index(request):
  return render_to_response('ldb/dashboard.html', post_data)