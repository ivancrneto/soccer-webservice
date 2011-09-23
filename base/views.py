from django.shortcuts import render_to_response
from django.template import Context, Template, RequestContext
from django.http import HttpResponseRedirect

def bla(request):
    return render_to_response('bla.html', locals())
