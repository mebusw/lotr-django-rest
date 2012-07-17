from django.db import models
from django.contrib import admin

# Create your models here.
class Poll(models.Model):
    title = models.CharField(max_length=150)
    body = models.TextField()
    timestamp = models.DateTimeField()
    like = models.IntegerField()
    
    
admin.site.register(Poll)
