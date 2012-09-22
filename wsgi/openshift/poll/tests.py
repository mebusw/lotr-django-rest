"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase
from django.utils import timezone
from models import Poll, Choice

import logging
logger = logging.getLogger('myproject.custom')

class PollModelTest(TestCase):
    def test_creating_a_new_poll_and_saving_it_to_the_database(self):
        poll = Poll()
        poll.question = "What's up?"
        poll.pub_date = timezone.now()
        
        poll.save()
        
        all_polls_in_database = Poll.objects.all()
        self.assertEquals(len(all_polls_in_database), 1)
        only_poll_in_database = all_polls_in_database[0]
        self.assertEquals(only_poll_in_database, poll)
        
        self.assertEquals(only_poll_in_database.question, "What's up?")
        self.assertEquals(only_poll_in_database.pub_date, poll.pub_date)
    
class ChoiceModelTest(TestCase):
    def test_choice_defaults(self):
        choice = Choice()
        self.assertEquals(choice.votes, 0)

class RestViewTest(TestCase):
    def test_root_url(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home/home.html')
        self.failUnlessEqual(response.status_code, 200)

    def test_about_url(self):
        # don't forget the last '/' of '/about/'
        response = self.client.get('/about/')
        self.assertTemplateUsed(response, 'about/about.html')

    def test_root_url_shows_all_polls(self):
        poll1 = Poll(question='6 times 7', pub_date=timezone.now())
        poll1.save()
        poll2 = Poll(question='life, the universe and everything', pub_date=timezone.now())
        poll2.save()

        response = self.client.get('/poll/polls/')
        ##logger.info(response)
        self.assertTemplateUsed(response, 'index.html')

        # check we've passed the polls to the template
        polls_in_context = response.context['latest_poll_list']
        ##logger.info(response.context)
        self.assertEquals(list(polls_in_context), [poll1, poll2])

        # check the poll names appear on the page
        self.assertIn(poll1.question, response.content)
        self.assertIn(poll2.question, response.content)
        
class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

    def test_basic_multiple(self):
        self.assertEqual(3 * 2, 6)
        