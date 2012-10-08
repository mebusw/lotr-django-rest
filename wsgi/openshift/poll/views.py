#!/usr/bin/python
# -*- coding: utf-8 -*-  
import os
from django.shortcuts import render_to_response, render, get_object_or_404
from poll.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from djangorestframework.views import View 
from django.core.context_processors import csrf
import simplejson as json
import django.contrib.auth
from forms import *
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.utils import timezone

import logging
logger = logging.getLogger('myproject.custom')
    
def index(request):
    latest_poll_list = cache.get('latest_poll_list')
    isFromCache = True
    if None == latest_poll_list:
        latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
        cache.set('latest_poll_list', latest_poll_list, 2)
        isFromCache = False
        #logger.info('refresh cache')

    context = {'latest_poll_list': latest_poll_list, 'dt':str(timezone.now()), 'isFromCache':isFromCache}
    return render(request, 'index.html', context)
    
def poll(request, poll_id):
    if request.method == 'POST':
        choice = Choice.objects.get(id=request.POST['vote'])
        choice.votes += 1
        choice.save()
        return HttpResponseRedirect(reverse('poll.views.poll', args=[poll_id,]))
        
    p = get_object_or_404(Poll, pk=poll_id)
    form = PollVoteForm(poll=p)
    return render(request, 'poll.html', {'poll': p, 'form': form})
    
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

def upload_file(request):
    #logger.info(settings.MEDIA_ROOT)

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        #logger.info(request.POST)
        #logger.info(dir(request.FILES['file']))
        #logger.info(form.errors)
        if form.is_valid():
            _handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect(reverse('poll.views.index'))
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def _handle_uploaded_file(f):
    destination = open(settings.MEDIA_ROOT + f.name, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

@cache_page(3)    #3 seconds
def login(request):
    ##rrr = {}
    ##rrr.update(csrf(request))
    ##return render_to_response('login.html', rrr)
    return render(request, 'login.html')

@login_required    
def userinfo(request):
    ###username = request.POST['username']
    ###password = request.POST['password']
    user = request.user

    ###user = django.contrib.auth.authenticate(username=username, password=password)
    return render(request, 'userinfo.html', {'s':dir(user), 'u':user.username, 
                                                    'p':user.password, 'is':user.is_authenticated,
                                                    'all_perms':user.get_all_permissions, 'groups':user.groups.all, 
                                                    'user_perms':user.user_permissions.all, 'group_perms':user.get_group_permissions})


# Customerized REST view
class RESTforPollAndChoice(View):  
    def get(self, request, *args, **kwargs):  
        return 'GET pid=%s cid=%s args=%s req=%s' % (kwargs['pid'], kwargs['cid'], args, request.GET)
    def delete(self, request, *args, **kwargs):  
        return 'DELETE pid=%s cid=%s args=%s req=%s' % (kwargs['pid'], kwargs['cid'], args, request.POST)
    def put(self, request, *args, **kwargs):  
        return 'PUT pid=%s cid=%s args=%s req=%s' % (kwargs['pid'], kwargs['cid'], args, request.POST)
    def post(self, request, *args, **kwargs):  
        return 'POST pid=%s cid=%s args=%s req=%s' % (kwargs['pid'], kwargs['cid'], args, request.POST)

class RESTforPoll(View):  
    def get(self, request, *args, **kwargs):
        pl = Poll.objects.all().order_by('-pub_date')[:5]
        pp=[]
        for p in pl:
            pp.append(p.question)
        return pp


