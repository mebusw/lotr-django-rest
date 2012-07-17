import os
from django.shortcuts import render_to_response
from poll.models import Poll

def list_polls(request):
    output = []
    for p in Poll.objects.all():
        o = {}
        o['title'] = p.title
        o['body'] = p.body
        o['timestamp'] = p.timestamp
        o['like'] = p.like
        output.append(o)
    return render_to_response('poll.html', {'polls': output})