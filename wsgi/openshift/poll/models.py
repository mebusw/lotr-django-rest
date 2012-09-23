# -*- coding: utf-8 -*-
from django.db import models
import logging

logger = logging.getLogger('myproject.custom')

# Create your models here.
class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    
    def __str__(self):
        return self.question.encode('utf-8')

    def total_votes(self):
        return sum(c.votes for c in self.choice_set.all())

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField(verbose_name="VOTES", default=0)

    def __str__(self):
        logger.info('calling Choice.__str__')
        return self.choice.encode('utf-8')

    def __unicode__(self):
        logger.info('calling Choice.__unicode__')
        return self.choice.encode('utf-8')
        
    def percentage(self):
        total_votes_on_poll = sum(c.votes for c in self.poll.choice_set.all())
        try:
            return 100.0 * self.votes / total_votes_on_poll
        except ZeroDivisionError:
            return 0    

class Cycle(models.Model):
    name = models.CharField(max_length=150)
    en_name = models.CharField(max_length=150)

    def __str__(self):
        logger.info('calling Cycle.__str__')
        return self.choice.encode('utf-8')

    def __unicode__(self):
        logger.info('calling Cycle.__unicode__')
        return self.choice.encode('utf-8')

        
class Package(models.Model):
    name = models.CharField(max_length=150)
    en_name = models.CharField(max_length=150)
    type = models.CharField(max_length=10, choices=(('core', 'core'), ('adv', 'adv'), ('duluxe', 'duluxe')))
    cycle = models.ForeignKey(Cycle)
    release_date = models.DateField()
    
    def __str__(self):
        return self.name.encode('utf-8')
    
class Scenario(models.Model):
    name = models.CharField(max_length=150)
    en_name = models.CharField(max_length=150)
    package_id = models.ForeignKey(Package)
    package_id = models.ForeignKey(Cycle)
    difficult_level = models.IntegerField()

    def __str__(self):
        return self.name.encode('utf-8')
    
class Session(models.Model):
    scenario_id = models.ForeignKey(Package)
    # scenario_name = models.CharField(max_length=150)
    session_date = models.DateField()
    heroes = models.CharField(max_length=150)
    win = models.IntegerField(choices=((1, 'Y'), (0, 'N')))
    score = models.IntegerField()

    def __str__(self):
        return '%s 战报: %d分' % (self.session_date, self.score)

