from django.contrib import admin

from .models import * 

__author__ = "Louis Dijkstra"

"""
	All models/tables accessible through the admin site
	are added here
"""

class StorageLocationInline(admin.TabularInline):
    model = StorageLocation
    extra = 1

class FileAdmin(admin.ModelAdmin): 
	inlines = (StorageLocationInline,) 

admin.site.register(Drive)
admin.site.register(DriveCopy)
admin.site.register(Person)
admin.site.register(Experiment)
admin.site.register(Format)
admin.site.register(Location)
admin.site.register(Sensor)
admin.site.register(File, FileAdmin)
admin.site.register(Source)
admin.site.register(StorageLocation)
