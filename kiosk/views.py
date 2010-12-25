from django.shortcuts import render_to_response
from django.template.context import RequestContext
from kiosk.models import History, StreamRequest

def live(request):
    ctx = { 'now' : History.objects.get_latest(),
            'request': StreamRequest.objects.get_new_request()}

    return render_to_response('kiosk_live.html',
                              ctx,
                              context_instance=RequestContext(request))
    
def select(request):
    return render_to_response('select.html',
                              {},
                              context_instance=RequestContext(request))