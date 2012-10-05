from django.contrib import admin
from models import *  


class PackageInline(admin.TabularInline):
    model = Package
    extra = 3

class CycleAdmin(admin.ModelAdmin):
    inlines = [PackageInline]

admin.site.register(Package)
admin.site.register(Cycle, CycleAdmin)
admin.site.register(Card)
