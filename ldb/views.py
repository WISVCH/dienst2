from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext


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
                ('#/committees', 'Commissies'),
                ('#/export', 'Exporteren')
            ]
        }
    }

    if request.user.has_module_perms('admin'):
        post_data['navbar']['items'].append((reverse('admin:ldb_person_changelist'), "Beheer"))

    return render_to_response('ldb/dashboard.html', post_data, context_instance=RequestContext(request))
