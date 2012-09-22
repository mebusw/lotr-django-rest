#!/usr/bin/python
# -*- coding: utf-8 -*-  
import os
from django.shortcuts import render_to_response, render
from django.shortcuts import get_object_or_404
from poll.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from djangorestframework.views import View 
from django.core.context_processors import csrf
import simplejson as json
import django.contrib.auth

import logging
logger = logging.getLogger('myproject.custom')
    
def index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    context = {'latest_poll_list': latest_poll_list}
    return render(request, 'index.html', context)
    
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
        return HttpResponseRedirect(reverse('poll.views.results', args=(p.id, )))
        
def results(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('results.html', {'poll': p})

def login(request):
    rrr = {}
    rrr.update(csrf(request))
    return render_to_response('login.html', rrr)

def userinfo(request):
    username = request.POST['username']
    password = request.POST['password']
    user = django.contrib.auth.authenticate(username=username, password=password)
    if user is not None:
        django.contrib.auth.login(request, user)
        return render_to_response('userinfo.html', {'s':dir(user), 'u':user.username, 
                                                    'p':user.password, 'is':user.is_authenticated,
                                                    'perm':user.get_all_permissions})
#        return render_to_response('userinfo.html', context_instance=RequestContext(request))

    else:
        return HttpResponseRedirect(reverse('poll.views.login'))




# Customerized REST view
class RESTforPollAndChoice(View):  
    def get(self, request, *args, **kwargs):  
        return 'get pid=%s cid=%s' % (kwargs['pid'], kwargs['cid'])
    def delete(self, request, *args, **kwargs):  
        return 'delete pid=%s cid=%s' % (kwargs['pid'], kwargs['cid'])
    def put(self, request, *args, **kwargs):  
        return 'put pid=%s cid=%s' % (kwargs['pid'], kwargs['cid'])
    def post(self, request, *args, **kwargs):  
        return 'post pid=%s cid=%s' % (kwargs['pid'], kwargs['cid'])

class RESTforPoll(View):  
    def get(self, request, *args, **kwargs):
        pl = Poll.objects.all().order_by('-pub_date')[:5]
        pp=[]
        for p in pl:
            pp.append(p.question)
        return json.dumps(pp)


