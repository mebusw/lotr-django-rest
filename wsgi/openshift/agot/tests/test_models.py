from django.test import TestCase
from django.utils import timezone
from datetime import datetime, time, date, timedelta
from poll.models import *
from agot.models import *
from django.db.models import Q, F   

import logging
logger = logging.getLogger('myproject.custom')

class CycleModelTest(TestCase):
    def setUp(self):
        cycle = Cycle(name='cycle1')
        cycle.save()
        
    def test_creating_and_saving(self):
        all_cycles = Cycle.objects.all()
        self.assertEqual(1, len(all_cycles))
        self.assertEqual('cycle1', all_cycles[0].name)

    def test_package_count(self):
        all_cycles = Cycle.objects.all()
        self.assertEqual(0, all_cycles[0].package_set.count())

    def test_unicode_display(self):
        all_cycles = Cycle.objects.all()
        self.assertEqual('cycle1', unicode(all_cycles[0]))

class CardModelTest(TestCase):
    def setUp(self):
        self.package = Package.objects.create(name='abc', cycle=None, pub_date=timezone.now(), type=u'基础')
        self.house = House.objects.create(name='Stark')
        self.card = Card.objects.create(name='sword', package=self.package, type=u'附属牌', cost=2)
        self.card.house.add(self.house)
        
    def test_creating_and_saving(self):
        all_cards= Card.objects.all()
        self.assertEqual('sword', all_cards[0].name)
        self.assertEqual(2, all_cards[0].cost)
        self.assertEqual(0, all_cards[0].strength)
        
        self.assertIn(self.house, all_cards[0].house.all())
        
