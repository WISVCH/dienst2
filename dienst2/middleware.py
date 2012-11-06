from django.conf import settings
from django.contrib.auth.views import login
from django.http import HttpResponseRedirect

class RequireLoginMiddleware(object):
    """
    Require Login middleware. If enabled, each Django-powered page will
    require authentication.
    
    http://djangosnippets.org/snippets/136/
    http://stackoverflow.com/questions/2164069/best-way-to-make-djangos-login-required-the-default
    """
    def __init__(self):
        self.require_login_path = getattr(settings, 'LOGIN_URL', '/accounts/login/')
    
    def process_request(self, request):
        if request.path != self.require_login_path and request.user.is_anonymous():
            if request.POST:
                return login(request)
            else:
                return HttpResponseRedirect('%s?next=%s' % (self.require_login_path, request.path))
