from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from kiosk.models import History, StreamRequest, STREAM_CHOICES
from django.http import HttpResponse

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

def set(request):
    if request.method == 'POST':
        sr = get_object_or_404(StreamRequest, id=request.POST['id'])
        state = request.POST['state']
        if state in [s for (s,name) in STREAM_CHOICES]:
            sr.state = state
            sr.save()
            return HttpResponse(status = 200)
    return HttpResponse(status = 400)
        
    