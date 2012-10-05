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
    cycle = models.ForeignKey(Cycle)
    pub_date = models.DateTimeField()
    type = models.CharField(max_length=1, choices=(('基础', '基础'), ('大扩', '大扩'), ('小扩', '小扩')), )
    
    def __unicode__(self):
        return self.name    
            
        
class Card(models.Model):
    name = models.CharField(max_length=255)
    package = models.ForeignKey(Package)
    cost = models.IntegerField()
    rules = models.TextField()
    img_path = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.name    
    