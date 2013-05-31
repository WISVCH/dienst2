from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
  return render_to_response('dienst2/dashboard.html', {'title': 'Dashboard'}, context_instance=RequestContext(request))
