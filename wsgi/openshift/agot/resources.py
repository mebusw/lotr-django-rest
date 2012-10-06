from django.core.urlresolvers import reverse  
from djangorestframework.views import View  
from djangorestframework.resources import ModelResource  
from models import *  
from djangorestframework.renderers import DocumentingPlainTextRenderer

class CycleItemResource(ModelResource):  
    model = Cycle  
    fields = ('name', 'packages')
    
    def packages(self, instance):
        return instance.package_set
        #return reverse('index', args=[instance.id])

class PackageItemResource(ModelResource):  
    model = Package  
    fields = ('name', 'type', 'cycle', 'pub_date', 'cards')
    ordering = ('-pub_date',)

    def cycle(self, instance):
        return instance.cycle

    def cards(self, instance):
        return instance.card_set
        
class CardItemResource(ModelResource):  
    model = Card  
    fields = ('name', 'package', 'cost', 'rules', 'house')

    def package(self, instance):
        return instance.package
        