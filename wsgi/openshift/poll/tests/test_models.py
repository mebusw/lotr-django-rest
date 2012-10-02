from django.test import TestCase
from django.utils import timezone
from datetime import datetime, time, date, timedelta
from poll.models import *
from django.db.models import Q, F   

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

    def test_relationships_backwards(self):
        p = Poll(question='where', pub_date=timezone.now())
        p.save()
        c1 = Choice(poll=p, choice='here', votes=0)
        c1.save()
        c2 = Choice(poll=p, choice='there', votes=0)
        c2.save()
        
        self.assertEquals(2, p.choice_set.count())
        
class ChoiceModelTest(TestCase):
    def test_choice_defaults(self):
        choice = Choice()
        self.assertEquals(choice.votes, 0)

class ManyToManyModelThroughAModelTest(TestCase):
    def test_many_to_many_through_a_model(self):
        ringo = Person.objects.create(name="Ringo Starr")
        paul = Person.objects.create(name="Paul McCartney")
        beatles = Group.objects.create(name="The Beatles")
        m1 = Membership(person=ringo, group=beatles, date_joined=date(1962, 8, 16), invite_reason="Needed a new drummer.")
        m1.save()
        
        self.assertEqual(1, len(beatles.members.all()))
        self.assertEqual("Ringo Starr", beatles.members.all()[0].name)
        self.assertEqual("The Beatles", ringo.group_set.all()[0].name)

class ManyToManyModelDirectlyTest(TestCase):
    def setUp(self):
        blog = Blog(name='Beatles Blog', tagline='All the latest Beatles news.')
        blog.save()
        entry = Entry.objects.create(headline='UFO found', blog=blog, pub_date=datetime.now(), mod_date=datetime.now(), n_comments=5, n_pingbacks=3, rating=5)
        john = Author.objects.create(name="John")
        paul = Author.objects.create(name="Paul", gender='Female')
        george = Author.objects.create(name="George", gender='Female')
        ringo = Author.objects.create(name="Ringo")
        entry.authors.add(john, paul, george, ringo)
    
        entry2 = Entry(headline='A song of ice and fire', blog=blog, pub_date=datetime.now(), mod_date=datetime.now(), n_comments=15, n_pingbacks=23, rating=5)        
        entry2.save()
        entry2.authors = [john, ringo]
    
    def test_relationships(self):
        entries = Entry.objects.all()[:2]
        entry1 = entries[0]
        entry2 = entries[1]
        self.assertEqual(4, entry1.authors.count())
        self.assertEqual(2, entry2.authors.count())

        author1 = Author.objects.get(pk=1)
        author2 = Author.objects.get(pk=2)
        self.assertEqual(2, author1.entry_set.count())
        self.assertEqual(1, author2.entry_set.count())
        
           
    def test_basic_filter(self):
        self.assertEqual(3, len(Author.objects.filter(name__contains='o')))
        self.assertEqual(2, len(Entry.objects.filter(blog__name__iexact='beatles blog')))
        
        filtered_author = self.name_map_helper(Author.objects.filter(name__contains='o', name__icontains='r'))
        self.assertEqual([u'George', u'Ringo'], filtered_author)
        
        filtered_author = self.name_map_helper(Author.objects.filter(name__contains='o').filter(gender='Female'))
        self.assertEqual([u'George'], filtered_author)

    def test_complex_filter(self):
        filtered_author = self.name_map_helper(Author.objects.filter(Q(name__contains='o') | Q(gender='Female')))
        self.assertEqual([u'John', u'Paul', u'George', u'Ringo'], filtered_author)        
        
    def test_filter_with_reference_fields(self):
        filtered_entry = Entry.objects.filter(rating__lt=F('n_comments') + F('n_pingbacks'))
        self.assertEqual(2, len(filtered_entry))
        
    def test_filter_with_pk_lookup(self):
        filtered_author = self.name_map_helper(Author.objects.filter(pk__in=[1, 2]))
        self.assertEqual([u'John', u'Paul'], filtered_author)
        
        filtered_author = self.name_map_helper(Author.objects.filter(id=3))
        self.assertEqual([u'George'], filtered_author)

    def test_delete_object(self):
        author  = Author.objects.get(pk=1)
        self.assertEqual(3, len(Author.objects.filter(name__contains='o')))
        author.delete()
        self.assertEqual(2, len(Author.objects.filter(name__contains='o')))
        

    def name_map_helper(self, lst):
        return map(lambda x: unicode(x), lst)