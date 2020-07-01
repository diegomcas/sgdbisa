from django.db import models
from django.contrib.auth.models import User
from documental.models import Documento

class ListaChequeo(models.Model):
    """
    Modelo que define una lista de chequeo y la describe según:
    area = El area de la empresa donde es aplicable
    tipo_documento = Para que tipo de documento está creado (Plano, informe, etc)
    nombre = un nombre característico para el tipo de chequeo
    """
    area = models.CharField(
        null=False,
        max_length=255,
        help_text="Área de la empresa donde se aplica el chequeo"
    )
    tipo_documento = models.CharField(
        default="PLANO",
        null=False,
        max_length=255,
        help_text="Tipos de documentos donde se aplica el check list"
    )
    nombre = models.CharField(
        null=False,
        max_length=255,
        help_text="Nombre de la lista de Verificación"
    )
    descripcion = models.CharField(
        'Descripción',
        null=True,
        max_length=1000,
        help_text="Descripción detallada de la Lista de Verificación"
    )
    tipos_chequeo = models.ManyToManyField(
        'TipoChequeo',
        blank=True,
        related_name='tipos_chequeo',
        help_text="Verificación a realizar"
    )

    class Meta:
        indexes = [
            models.Index(fields=['area', 'tipo_documento', 'nombre']),
        ]
        ordering = ['area', 'tipo_documento', 'nombre']
        permissions = (
            ('list_listaschequeo', 'Can list listas chequeo'),
        )

    def __str__(self):
        return self.area + "." + self.tipo_documento + "." + self.nombre


class TipoChequeo(models.Model):
    """
    Modelo que define un Tipo de Chequeo
    con sus características generales.
    """
    nombre = models.CharField(
        null=False,
        default='',
        max_length=255,
        help_text="Nombre de la Verificación a realizar"
    )
    ayuda = models.CharField(
        null=True,
        max_length=1000,
        help_text="Descripción detallada de la Verificación"
    )

    class Meta:
        indexes = [
            models.Index(fields=['nombre']),
        ]
        ordering = ['nombre']
        permissions = (
            ('list_tiposchequeo', 'Can list tipos chequeo'),
        )

    def __str__(self):
        return self.nombre


class Chequeo(models.Model):
    """
    Modelo que define un chequeo para el documento (Plano, Informe, etc)
    con sus características generales.
    """
    verificado = models.BooleanField(
        default=False
    )
    aplica = models.BooleanField(
        default=True
    )
    documento = models.ForeignKey(
        'documental.Documento',
        related_name='documento',
        default=0,
        on_delete=models.CASCADE,
        help_text="Documento al que pertenece el check"
    )
    tipo_chequeo = models.ForeignKey(
        'TipoChequeo',
        related_name='tipo_chequeo',
        on_delete=models.DO_NOTHING,
        help_text="Verificación a realizar"
    )
    verificado_por = models.ForeignKey(
        User,
        related_name='verificado_por',
        default=None,
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
        help_text="Persona que realizó la verificación"
    )

    class Meta:
        indexes = [
            models.Index(fields=['documento']),
        ]
        ordering = ['documento']

    def __str__(self):
        return '' + self.documento.numero + ' - ' + self.tipo_chequeo.nombre
