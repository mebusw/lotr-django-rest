from django.contrib import admin
from models import *  

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