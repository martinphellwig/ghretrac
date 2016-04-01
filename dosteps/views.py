from django.shortcuts import render, render_to_response
from django.http.response import HttpResponse
from django.template import RequestContext

def root(request):
    context = {'html':{'head':{'title':'Hello World Title!'}}}
    template = 'root.html'
    
    return render_to_response(template, context, 
                              context_instance=RequestContext(request))
