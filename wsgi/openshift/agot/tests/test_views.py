# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase
from django.utils import timezone
from agot.models import *
from django.contrib.auth.models import User
import django.contrib.auth
from django.core.cache import cache

import logging
logger = logging.getLogger('myproject.custom')


