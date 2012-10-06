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

        
