from django.core.urlresolvers import reverse  
from djangorestframework.views import View  
from djangorestframework.resources import ModelResource  
from models import *  
from djangorestframework.renderers import DocumentingPlainTextRenderer

class ChoiceItemResource(ModelResource):  
    model = Choice  
    fields = ('poll', 'choice', 'vote')
    #ordering = ('-created',)
    
    def poll(self, instance):
        #return reverse('poll', kwargs={'question': instance.poll.question})
        #return  instance.poll.question
        return instance.poll

class PollItemResource(ModelResource):  
    model = Poll  
    fields = ('question', 'choices', 'pub_date')
    ordering = ('-pub_date',)
    
    def choices(self, instance):
        return instance.choice_set    
        #return reverse('choice', kwargs={'choice': 'no'})
