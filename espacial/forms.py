from django.contrib.gis import forms
from .models import ElementoEspacial

class ElementoEspacialForm(forms.Form):
    tipo_elemento = forms.ChoiceField(
        required=True,
    )
    puntos = forms.CharField(
        label='puntos',
        max_length=1000,
        widget=forms.Textarea
    )
    poligono = forms.CharField(
        label='poligono',
        max_length=1000,
        widget=forms.Textarea
    )
