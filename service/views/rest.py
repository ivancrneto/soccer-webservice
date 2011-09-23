from django.shortcuts import render_to_response
from django.template import Context, Template, RequestContext
from django.http import HttpResponseRedirect

class RestView(object):
    allowed_methods = ('GET', 'PUT', 'POST', 'DELETE', 'HEAD', 'OPTIONS')

    def __call__(self, request, *args, **kwargs):
        method = nonalpha_re.sub('', request.method.upper())
        if not method in self.allowed_methods or not hasattr(self, method):
            return self.method_not_allowed(method)
        return getattr(self, method)(request, *args, **kwargs)

    def method_not_allowed(self, method):
        response = HttpResponse('Method not allowed: %s' % method)
        response.status_code = 405
        return response
        
        
class EventView(RestView):
    def GET(self, request, event_id):
        pass
        
def bli(request):
    return render_to_response('service_bla.html', {'resource': 'rest'})
