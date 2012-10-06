from django.contrib import admin
from models import *  


class PackageInline(admin.TabularInline):
    model = Package
    extra = 3

class CycleAdmin(admin.ModelAdmin):
    inlines = [PackageInline]

    
class CardInline(admin.TabularInline):
    model = Card
    extra = 2

class PackageAdmin(admin.ModelAdmin):
    inlines = [CardInline]

    
admin.site.register(Cycle, CycleAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(Card)
