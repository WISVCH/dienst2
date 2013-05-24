from django.shortcuts import render_to_response

post_data = {
  'title': 'Kasbeheer', 
  'ng_app': 'kas',
  'navbar': {
    'title': 'Kasbeheer',
    'items': [
      ('#/transactions', 'Transacties'),
      ('#/closures', 'Dagafsluitingen'),
      ('#/barcode', 'Barcode Tool'),
    ]
  }
}

import urls


def index(request):
  return render_to_response('kas/dashboard.html', post_data)