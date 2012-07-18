from django.db import models
from django.contrib import admin

# Create your models here.
class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField()

    
class Cycle(models.Model):
    name = models.CharField(max_length=150)
    en_name = models.CharField(max_length=150)
    #package_id = models.IntegerField()

class Package(models.Model):
    name = models.CharField(max_length=150)
    en_name = models.CharField(max_length=150)
    type = models.CharField(max_length=10)
    cycle = models.ForeignKey(Cycle)
    release_date = models.DateField()
    
    
class Scenario(models.Model):
    name = models.CharField(max_length=150)
    en_name = models.CharField(max_length=150)
    package_id = models.ForeignKey(Package)
    package_id = models.ForeignKey(Cycle)
    difficult_level = models.IntegerField()
    
class Session(models.Model):
    scenario_id = models.ForeignKey(Package)
    # scenario_name = models.CharField(max_length=150)
    session_date = models.DateField()
    heroes = models.CharField(max_length=150)
    win = models.IntegerField()
    score = models.IntegerField()

##########

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3

class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]

admin.site.register(Poll, PollAdmin)
admin.site.register(Choice)


class PackageInline(admin.TabularInline):
    model = Package
    extra = 3

class CycleAdmin(admin.ModelAdmin):
    inlines = [PackageInline]

admin.site.register(Package)
admin.site.register(Cycle, CycleAdmin)
admin.site.register(Scenario)
admin.site.register(Session)
