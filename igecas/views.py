from django.shortcuts import render, render_to_response
from django.http.response import HttpResponse
from django.template import RequestContext

def index(request):
    context = {'html':{'head':{'title':'Hello World Title!'}}}
    template = 'igecas/index.html'
    
    return render_to_response(template, context, 
                              context_instance=RequestContext(request))
