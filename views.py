from django.shortcuts import render_to_response
from django.template import RequestContext

def test(request):
    return render_to_response('django_tagcapsule/test.html', {'val': '"I was set in the view !"'}, context_instance=RequestContext(request))
    