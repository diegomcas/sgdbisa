from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import ElementoEspacial

# Register your models here.
admin.site.register(ElementoEspacial)
class ElementoEspacialAdmin(OSMGeoAdmin):
    list_display = ('name', 'location')
