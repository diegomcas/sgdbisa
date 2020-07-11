from django import forms
from django.forms import ModelForm, ModelMultipleChoiceField
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import Proyecto, Documento, Archivo, User


class MyDateInput(forms.DateInput):
    input_type = 'date'

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%d"
        super().__init__(**kwargs)


class ProyectoForm(ModelForm):
    """
    Definiciones generales de los formularios que controlan el modelo Proyecto
    """
    fecha = forms.DateField(
        widget=MyDateInput(attrs={'type': 'date'}),
        help_text="Fecha de inicio del proyecto"
    )

    descripcion = forms.CharField(
        max_length=1000,
        widget=forms.Textarea(attrs={'cols': 80, 'rows': 4}),
        help_text="Breve descripción del Trabajo"
    )

    miembros = ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=FilteredSelectMultiple("Miembros", is_stacked=False)
    )

    class Meta:
        model = Proyecto
        exclude = ['finalizado']


class DocumentoForm(ModelForm):
    """
    Definiciones generales de los formularios que controlan el modelo Documento
    """
    fecha = forms.DateField(
        widget=MyDateInput(attrs={'type': 'date'}),
        help_text="Fecha del documento (la que se define en el rótulo)"
    )

    descripcion = forms.CharField(
        max_length=1000,
        widget=forms.Textarea(attrs={'cols': 80, 'rows': 2}),
        help_text="Breve descripción del Trabajo"
    )

    refiere_a = ModelMultipleChoiceField(
        queryset=None,
        widget=FilteredSelectMultiple("Refiere a: Documentos", is_stacked=False),
        required=False,
    )

    compuesto_por = ModelMultipleChoiceField(
        queryset=None,
        widget=FilteredSelectMultiple("Compuesto por: archivos", is_stacked=False),
        required=False,
    )

    class Meta:
        model = Documento
        exclude = ['proyecto', 'reemplaza_a', 'reemplazado_por', 'espacial', ]

    def __init__(self, project, *args, **kwargs):
        super(DocumentoForm, self).__init__(*args, **kwargs)
        self.fields['propietario'].queryset = project.miembros.all()
        self.fields['refiere_a'].queryset = Documento.objects.filter(proyecto__pk=project.pk)
        self.fields['compuesto_por'].queryset = Archivo.objects.filter(proyecto__pk=project.pk)
        # self.fields['refiere_a'].empty_label = '-------'
        # self.fields['compuesto_por'].empty_label = '-------'


class ArchivoForm(ModelForm):
    """
    Definiciones generales de los formularios que controlan los archivos
    """
    nombre_archivo = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

    fecha_edicion = forms.DateField(
        widget=MyDateInput(attrs={'type': 'date', 'readonly': 'readonly'}),
        help_text="Fecha de edición del archivo."
    )

    descripcion = forms.CharField(
        max_length=1000,
        widget=forms.Textarea(attrs={'cols': 80, 'rows': 2}),
        help_text="Breve descripción del Archivo"
    )

    archivo_compone_a = ModelMultipleChoiceField(
        queryset=None,
        widget=FilteredSelectMultiple("Compone a: documentos", is_stacked=False),
        required=False,
    )

    class Meta:
        model = Archivo
        fields = (
            'nombre_archivo',
            'fecha_edicion',
            'revision',
            'directorio',
            'tipo_representacion',
            'propietario',
            'descripcion',
            'archivo_compone_a',
        )
        # exclude = ['proyecto', 'fecha_creacion', 'reemplaza_a', 'reemplazado_por', 'hash_archivo', ]

    def __init__(self, project, *args, **kwargs):
        super(ArchivoForm, self).__init__(*args, **kwargs)
        self.fields['propietario'].queryset = project.miembros.all()
        self.fields['archivo_compone_a'].queryset = Documento.objects.filter(proyecto__pk=project.pk)

        print(self.instance)
        if self.instance and self.instance.pk:
            self.fields['archivo_compone_a'].initial = self.instance.archivos.all()

    def save(self, commit=True):
        archivo = super(ArchivoForm, self).save(commit=False)

        if commit:
            archivo.save()

        if archivo.pk:
            archivo.archivos.set(self.cleaned_data['archivo_compone_a'])
            self.save_m2m()

        return archivo
