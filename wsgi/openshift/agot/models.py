# -*- coding: utf-8 -*-
from django.db import models
import logging

logger = logging.getLogger('myproject.custom')

class Trait(models.Model):
    name = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.name    
    
class Keyword(models.Model):
    name = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.name    

class House(models.Model):
    name = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.name    

class Crest(models.Model):
    name = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.name    
        
class Type(models.Model):
    name = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.name    
        
class Cycle(models.Model):
    name = models.CharField(max_length=255)
   
    def __unicode__(self):
        return self.name    

class Package(models.Model):
    name = models.CharField(max_length=255)
    cycle = models.ForeignKey(Cycle, null=True, blank=True)
    pub_date = models.DateField()
    type = models.CharField(max_length=10, choices=((u'基础', u'基础'), (u'大扩', u'大扩'), (u'小扩', u'小扩')), )
    
    def __unicode__(self):
        return self.name    
            
        
class Card(models.Model):
    name = models.CharField(max_length=255)
    package = models.ForeignKey(Package)
    type = models.CharField(max_length=10, choices=((u'附属牌', u'附属牌'), ))
    cost = models.IntegerField(default=0)
    house = models.ManyToManyField(House)
    strength = models.IntegerField(default=0)
    traits = models.ManyToManyField(Trait)
    rules = models.TextField()
    keywords = models.ManyToManyField(Keyword)
    crests = models.ManyToManyField(Crest)
    img_path = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.name    
    
    