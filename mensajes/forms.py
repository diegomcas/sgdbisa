from django.forms import ModelForm
from django import forms
from .models import Tique

class TiqueForm(ModelForm):
    descripcion = forms.CharField(
        max_length=1000,
        widget=forms.Textarea(attrs={'cols': 80, 'rows': 2}),
        help_text="Tareas a ejecutar."
    )

    class Meta:
        model = Tique
        fields = (
            'descripcion',
            'tipo_tique',
        )
