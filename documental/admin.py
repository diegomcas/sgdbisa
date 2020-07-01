from django.contrib import admin
from .models import Proyecto, Documento, Archivo

# Register your models here.
admin.site.register(Proyecto)
admin.site.register(Documento)
admin.site.register(Archivo)
