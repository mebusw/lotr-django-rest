from django.core.urlresolvers import reverse  
from djangorestframework.views import View  
from djangorestframework.resources import ModelResource  
from models import *  
from djangorestframework.renderers import DocumentingPlainTextRenderer

class CycleItemResource(ModelResource):  
    model = Cycle  
    fields = ('id', 'name', 'packages')
    
    def packages(self, instance):
        return instance.package_set
        #return reverse('index', args=[instance.id])

class PackageItemResource(ModelResource):  
    model = Package  
    fields = ('id', 'name', 'type', 'cycle', 'pub_date', 'cards')
    ordering = ('-pub_date',)

    def cycle(self, instance):
        return instance.cycle

    def cards(self, instance):
        return instance.card_set
        
class CardItemResource(ModelResource):  
    model = Card  
    fields = ('id', 'name', 'package', 'cost', 'rules', 'house')

    def package(self, instance):
        return instance.package
        