from django.core.urlresolvers import reverse  
from djangorestframework.views import View  
from djangorestframework.resources import ModelResource  
from models import Choice  


class LineItemResource(ModelResource):  
    model = Choice  
    fields = ('choice', 'vote')  
    #def product(self, instance):  
        #return instance.product.title  
