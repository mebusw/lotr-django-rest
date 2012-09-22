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

class MTVTest(TestCase):
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

    def test_login(self):
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
    
    def test_form_renders_poll_choices_as_radio_inputs(self):
        # set up a poll with a couple of choices
        poll1 = Poll(question='6 times 7', pub_date=timezone.now())
        poll1.save()
        choice1 = Choice(poll=poll1, choice='42', votes=0)
        choice1.save()
        choice2 = Choice(poll=poll1, choice='The Ultimate Answer', votes=0)
        choice2.save()

        # set up another poll to make sure we only see the right choices
        poll2 = Poll(question='time', pub_date=timezone.now())
        poll2.save()
        choice3 = Choice(poll=poll2, choice='PM', votes=0)
        choice3.save()

        # build a voting form for poll1
        form = PollVoteForm(poll=poll1)

        # check it has a single field called 'vote', which has right choices:
        self.assertEquals(form.fields.keys(), ['vote'])

        # choices are tuples in the format (choice_number, choice_text):
        self.assertEquals(form.fields['vote'].choices, [
            (choice1.id, choice1.choice),
            (choice2.id, choice2.choice),
        ])

        # check it uses radio inputs to render
        self.assertIn('input type="radio"', form.as_p())

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
        
class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

    def test_basic_multiple(self):
        self.assertEqual(3 * 2, 6)
        