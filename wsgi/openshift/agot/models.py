# -*- coding: utf-8 -*-
from django.db import models
import logging

logger = logging.getLogger('myproject.custom')

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
    cost = models.IntegerField()
    house = models.CharField(max_length=5, choices=((u'史塔克', u'史塔克'), (u'兰尼斯特', u'兰尼斯特'), ))
    strength = models.IntegerField()
    traits = models.CharField(max_length=5)
    rules = models.TextField()
    keywords = models.CharField(max_length=5)
    crests = models.CharField(max_length=5)
    img_path = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.name    
    