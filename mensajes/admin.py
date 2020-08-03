from django.contrib import admin
from .models import Mensaje, Tique, MensajeDestinatarios, TiqueDestinatarios

# Register your models here.
admin.site.register(Mensaje)
admin.site.register(Tique)
admin.site.register(MensajeDestinatarios)
admin.site.register(TiqueDestinatarios)
