from django.contrib import admin
from .models import ListaChequeo, TipoChequeo, Chequeo

# Register your models here.
admin.site.register(ListaChequeo)
admin.site.register(TipoChequeo)
admin.site.register(Chequeo)
