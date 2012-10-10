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

class PackgeViewTest(TestCase):
    ### fixtures = ['agot.json']

    def test_create_a_new_package_and_return_it(self):
        pkg = Package(name='abc', cycle=None, pub_date=timezone.now(), type=u'基础')
        pkg.save()
        response = self.client.get('/agot/package/')

        #logger.info(dir(response))
        self.assertEqual(200, response.status_code)
        self.assertIn('"name": "abc"', response.content)
        self.assertIn('"cycle": null', response.content)

        #self.assertTemplateUsed(response, 'index.html')
        #self.assertFalse(response.context['isFromCache'])

        #self.assertTemplateUsed(response, 'index.html')

class CardViewTest(TestCase):
    def test_(self):
        pass
        