from django import forms
from django.forms import ModelForm, ModelMultipleChoiceField
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import ListaChequeo, TipoChequeo, Chequeo


class ListaChequeoForm(ModelForm):
    """
    Definiciones generales de los formularios que controlan el modelo ListaChequeo
    """
    tipos_chequeo = ModelMultipleChoiceField(
        queryset=TipoChequeo.objects.all(),
        widget=FilteredSelectMultiple("Tipos de Chequeo", is_stacked=False),
        required=False,
    )

    class Meta:
        model = ListaChequeo
        fields = '__all__'


class TipoChequeoForm(ModelForm):
    """
    Definiciones generales de los formularios que controlan el modelo TipoChequeo
    """
    listas_chequeo = ModelMultipleChoiceField(
        queryset=ListaChequeo.objects.all(),
        widget=FilteredSelectMultiple("Listas de Chequeo", is_stacked=False),
        required=False,
    )

    class Meta:
        model = TipoChequeo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TipoChequeoForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['listas_chequeo'].initial = self.instance.listachequeo_tipos_chequeo.all()

    def save(self, commit=True):
        tipo_chequeo = super(TipoChequeoForm, self).save(commit=False)

        if commit:
            tipo_chequeo.save()

        if tipo_chequeo.pk:
            tipo_chequeo.listachequeo_tipos_chequeo.set(self.cleaned_data['listas_chequeo'])
            self.save_m2m()

        return tipo_chequeo
