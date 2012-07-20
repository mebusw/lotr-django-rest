#!/usr/bin/python
# -*- coding: utf-8 -*-  
import os
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from poll.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from djangorestframework.views import View 
from django.core.context_processors import csrf
    
def index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    return render_to_response('index.html', {'latest_poll_list': latest_poll_list})
    
    
def detail(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    #return render_to_response('detail.html', {'poll': p})
    return HttpResponse([p.pk, p.question])
    
def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        rrr = {}
        rrr.update(csrf(request))
        rrr['poll']=p
        rrr['error_message']="You didn't select a choice."
        return render_to_response('detail.html', rrr)
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('openshift.poll.views.results', args=(p.id, )))
        
def results(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('results.html', {'poll': p})

 

class RESTforAPoll(View):  
    def get(self, request, *args, **kwargs):  
        return 'get %s' % kwargs['id']
    def delete(self, request, *args, **kwargs):  
        return 'delete %s' % args['id']
    def put(self, request, *args, **kwargs):  
        return 'put %s' % args['id']

class RESTforPolls(View):  
    def get(self, request, *args, **kwargs):  
        return 'get all'
    def post(self, request, *args, **kwargs):  
        return 'post new'

