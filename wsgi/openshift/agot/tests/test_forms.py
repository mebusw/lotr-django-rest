"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase
from django.utils import timezone
from poll.models import Poll, Choice
from django.contrib.auth.models import User
from poll.forms import PollVoteForm

import logging
logger = logging.getLogger('myproject.custom')


        
class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

    def test_basic_multiple(self):
        self.assertEqual(3 * 2, 6)
        