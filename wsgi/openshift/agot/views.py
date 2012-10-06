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
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.utils import timezone

import logging
logger = logging.getLogger('myproject.custom')
    

