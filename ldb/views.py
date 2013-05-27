from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
import urls

def index(request):

  post_data = {
    'title': 'Ledendatabase', 
    'ng_app': 'ldb',
    'navbar': {
      'title': 'Ledendatabase',
      'items': [
        ('#/dashboard', 'Zoeken'),
        ('#/person/new', 'Nieuw Persoon'),
        ('#/organization/new', 'Nieuwe Organisatie'),
        ('#/export', 'Exporteren'),
        (reverse('admin:ldb_person_changelist'), "Beheer")
      ]
    }
  }

  return render_to_response('ldb/dashboard.html', post_data)