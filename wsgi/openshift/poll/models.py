# -*- coding: utf-8 -*-
from django.db import models
import logging

logger = logging.getLogger('myproject.custom')

# Create your models here.
class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    
    def __unicode__(self):
        return self.question

    def total_votes(self):
        return sum(c.votes for c in self.choice_set.all())

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField(verbose_name="VOTES", default=0)

    def __unicode__(self):
        return self.name
        
    def percentage(self):
        total_votes_on_poll = sum(c.votes for c in self.poll.choice_set.all())
        try:
            return 100.0 * self.votes / total_votes_on_poll
        except ZeroDivisionError:
            return 0    

class Cycle(models.Model):
    name = models.CharField(max_length=150)
    en_name = models.CharField(max_length=150)

    def __unicode__(self):
        return self.name

        
class Package(models.Model):
    name = models.CharField(max_length=150)
    en_name = models.CharField(max_length=150)
    type = models.CharField(max_length=10, choices=(('core', 'core'), ('adv', 'adv'), ('duluxe', 'duluxe')))
    cycle = models.ForeignKey(Cycle)
    release_date = models.DateField()
    
    def __unicode__(self):
        return self.name
    
class Scenario(models.Model):
    name = models.CharField(max_length=150)
    en_name = models.CharField(max_length=150)
    package_id = models.ForeignKey(Package)
    package_id = models.ForeignKey(Cycle)
    difficult_level = models.IntegerField()

    def __unicode__(self):
        return self.name
    
class Session(models.Model):
    scenario_id = models.ForeignKey(Package)
    # scenario_name = models.CharField(max_length=150)
    session_date = models.DateField()
    heroes = models.CharField(max_length=150)
    win = models.IntegerField(choices=((1, 'Y'), (0, 'N')))
    score = models.IntegerField()

    def __unicode__(self):
        return '%s 战报: %d分' % (self.session_date, self.score)



class Person(models.Model):
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name

    
class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person, through='Membership')

    def __unicode__(self):
        return self.name

class Membership(models.Model):
    person = models.ForeignKey(Person)
    group = models.ForeignKey(Group)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)
    

    
class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __unicode__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=(('Female', 'Female'), ('Male', 'Male')), default='Male')
    email = models.EmailField()

    def __unicode__(self):
        return self.name

class Entry(models.Model):
    blog = models.ForeignKey(Blog)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateTimeField()
    mod_date = models.DateTimeField()
    authors = models.ManyToManyField(Author)
    n_comments = models.IntegerField()
    n_pingbacks = models.IntegerField()
    rating = models.IntegerField()

    def __unicode__(self):
        return self.headline    