from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Mensaje(models.Model):
    """
    Modelo que define un mensaje con sus características generales.
    """
    mensaje = models.CharField(
        max_length=1000,
        null=False,
        help_text="Mensaje"
    )
    fecha = models.DateField(
        default=timezone.now,
        help_text="Fecha del mensaje"
    )

    class Meta:
        indexes = [
            models.Index(fields=['fecha', ]),
        ]
        ordering = ['-fecha', ]

class Tique(models.Model):
    """
    Modelo que define un tique con sus características generales.
    """
    OBSERVACION = 'OBS'
    REVISION = 'REV'
    TIPO_TIQUE_CHOICES = [
        (OBSERVACION, 'Observación'),
        (REVISION, 'Revisión'),
    ]

    descripcion = models.CharField(
        max_length=1000,
        null=False,
        help_text="Mensaje"
    )
    tipo_tique = models.CharField(
        max_length=3,
        choices=TIPO_TIQUE_CHOICES,
        default=OBSERVACION,
        help_text="Tipo corrección aplicable al Tique"
    )
    propietario = models.ForeignKey(
        User,
        related_name='propietario',
        null=True,
        on_delete=models.SET_NULL,
        help_text="Miembro del equipo de trabajo responsable de las correcciones"
    )
    finalizado = models.BooleanField(
        null=True,
    )
    fecha_emision = models.DateField(
        default=timezone.now,
        help_text="Fecha de emisión del tique"
    )
    fecha_adquisicion = models.DateField(
        null=True,
        help_text="Fecha en la que el usaurio acepta el tique"
    )
    fecha_finalización = models.DateField(
        null=True,
        help_text="Fecha en la que el usaurio finaliza el tique"
    )
    # destinatarios = models.ManyToManyField(
    #    User,
    #    related_name='destinatarios',
    #    help_text="Miembros del equipo de Proyecto"
    # )

    class Meta:
        indexes = [
            models.Index(fields=['fecha_emision', ]),
        ]
        ordering = ['-fecha_emision', ]
        permissions = (
            ("get_tique", "Can get a Tique"),
            ("finalize_tique", "Can finalize a Tique"),
        )

class MensajeDestinatarios(models.Model):
    """
    Modelo que define el estado de leido por cada uno de los miembros del proyecto
    del Documento o Archivo que referencia al mensaje.
    """
    mensaje = models.ForeignKey(
        'Mensaje',
        null=True,
        on_delete=models.SET_NULL,
        help_text="Mensaje"
    )
    miembro = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        help_text="Miembro del equipo de trabajo"
    )
    leido = models.BooleanField()

class TiqueDestinatarios(models.Model):
    """
    Modelo que define los miembros del proyecto
    del Documento o Archivo que referencia al tique.
    """
    tique = models.ForeignKey(
        'Tique',
        null=True,
        on_delete=models.SET_NULL,
        help_text="Tique"
    )
    miembro = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        help_text="Miembro del equipo de trabajo"
    )
