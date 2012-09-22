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

class PollsViewTest(TestCase):
    # python manage.py dumpdata auth.User --indent=2 > poll/fixtures/admin_user.json
    fixtures = ['admin_user.json']
    
    def test_root_url(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home/home.html')
        self.failUnlessEqual(response.status_code, 200)

    def test_about_url(self):
        # don't forget the last '/' of '/about/'
        response = self.client.get('/about/')
        self.assertTemplateUsed(response, 'about/about.html')

    def test_login_via_POST(self):
        response = self.client.post('/poll/polls/userinfo/', {'username': 'admin', 'password': 'admin'})
        self.assertTemplateUsed(response, 'userinfo.html')
        self.assertEquals('admin', response.context['u'])
        
    def test_django_auth(self):
        ##logger.info(User.objects.all())
        response = self.client.login(username='fred', password='secret')
        self.assertFalse(response)
        response = self.client.login(username='admin', password='admin')
        self.assertTrue(response)

    def test_poll_url_shows_all_polls(self):
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
    
    def test_page_shows_choices_using_form(self):
        # set up a poll with choices
        poll1 = Poll(question='time', pub_date=timezone.now())
        poll1.save()
        choice1 = Choice(poll=poll1, choice="PM", votes=0)
        choice1.save()
        choice2 = Choice(poll=poll1, choice="Gardener's", votes=0)
        choice2.save()

        response = self.client.get('/poll/polls/%d/' % (poll1.id, ))

        # check we've passed in a form of the right type
        self.assertTrue(isinstance(response.context['form'], PollVoteForm))
        self.assertTrue(response.context['poll'], poll1)
        self.assertTemplateUsed(response, 'poll.html')

        # and check the check the form is being used in the template,
        # by checking for the choice text
        self.assertIn(choice1.choice, response.content.replace('&#39;', "'"))
        self.assertIn(choice2.choice, response.content.replace('&#39;', "'"))
        self.assertIn('csrf', response.content)
        self.assertIn('0 %', response.content)

    def test_view_can_handle_votes_via_POST(self):
        # set up a poll with choices
        poll1 = Poll(question='6 times 7', pub_date=timezone.now())
        poll1.save()
        choice1 = Choice(poll=poll1, choice='42', votes=1)
        choice1.save()
        choice2 = Choice(poll=poll1, choice='The Ultimate Answer', votes=3)
        choice2.save()

        # set up our POST data - keys and values are strings
        post_data = {'vote': str(choice2.id)}

        # make our request to the view
        poll_url = '/poll/polls/%d/' % (poll1.id,)
        response = self.client.post(poll_url, data=post_data)

        # retrieve the updated choice from the database
        choice_in_db = Choice.objects.get(pk=choice2.id)

        # check it's votes have gone up by 1
        self.assertEquals(choice_in_db.votes, 4)
        self.assertEquals(choice_in_db.percentage(), 80)

        # always redirect after a POST - even if, in this case, we go back
        # to the same page.
        self.assertRedirects(response, poll_url)
        