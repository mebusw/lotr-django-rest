from django.test import TestCase
from django.utils import timezone
from datetime import datetime, time, date, timedelta
from poll.models import *


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

    def test_choice_can_calculate_its_own_percentage_of_votes(self):
        poll = Poll(question='who?', pub_date=timezone.now())
        poll.save()
        choice1 = Choice(poll=poll, choice='me', votes=2)
        choice1.save()
        choice2 = Choice(poll=poll, choice='you', votes=1)
        choice2.save()

        self.assertEquals(choice1.percentage(), 100 * 2 / 3.0)
        self.assertEquals(choice2.percentage(), 100 * 1 / 3.0)

        # also check 0-votes case
        choice1.votes = 0
        choice1.save()
        choice2.votes = 0
        choice2.save()
        self.assertEquals(choice1.percentage(), 0)
        self.assertEquals(choice2.percentage(), 0)

    def test_poll_can_tell_you_its_total_number_of_votes(self):
        p = Poll(question='where', pub_date=timezone.now())
        p.save()
        c1 = Choice(poll=p, choice='here', votes=0)
        c1.save()
        c2 = Choice(poll=p, choice='there', votes=0)
        c2.save()

        self.assertEquals(p.total_votes(), 0)

        c1.votes = 1000
        c1.save()
        c2.votes = 22
        c2.save()
        self.assertEquals(p.total_votes(), 1022)
        
class ChoiceModelTest(TestCase):
    def test_choice_defaults(self):
        choice = Choice()
        self.assertEquals(choice.votes, 0)

class ManyToManyModelTest(TestCase):
    def test_many_to_many_through_a_model(self):
        ringo = Person.objects.create(name="Ringo Starr")
        paul = Person.objects.create(name="Paul McCartney")
        beatles = Group.objects.create(name="The Beatles")
        m1 = Membership(person=ringo, group=beatles, date_joined=date(1962, 8, 16), invite_reason="Needed a new drummer.")
        m1.save()
        
        self.assertEqual(1, len(beatles.members.all()))
        self.assertEqual("Ringo Starr", beatles.members.all()[0].name)
        self.assertEqual("The Beatles", ringo.group_set.all()[0].name)


