from string import ascii_uppercase
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Proyecto(models.Model):
    """
    Modelo que define un proyecto con sus características generales.
    """
    orden_trabajo = models.CharField(
        max_length=50,
        null=False,
        help_text="Nro. Orden de Trabajo"
    )

    fecha = models.DateField(
        default=timezone.now,
        null=False,
        help_text="Fecha de inicio del Trabajo"
    )

    descripcion = models.CharField(
        'Descripción',
        max_length=1000,
        null=True,
        help_text="Breve descripción del Trabajo"
    )

    finalizado = models.BooleanField(
        default=False,
        help_text="Estado de finalización del Trabajo"
    )

    directorio = models.CharField(
        max_length=1000,
        null=False,
        help_text="Ubicación (Carpeta) del Trabajo"
    )

    miembros = models.ManyToManyField(
        User,
        help_text="Miembros del equipo de Proyecto"
    )

    class Meta:
        indexes = [
            models.Index(fields=['orden_trabajo', 'fecha']),
        ]
        ordering = ['fecha', 'orden_trabajo', ]
        permissions = (
            ('list_proyectos', 'Can list proyectos'),
            ('finalize_proyecto', 'Can finalize proyecto'),
        )

    def __str__(self):
        """
        Cadena que representa a la instancia particular del modelo
        (p. ej. en el sitio de Administración)
        """
        return self.orden_trabajo


class Documento(models.Model):
    """
    Modelo que define un documento (Plano, Informe, etc)
    con sus características generales.
    """
    numero = models.CharField(
        'Número',
        max_length=255,
        null=False,
        help_text="Nombre (Número) del Documento"
    )
    fecha = models.DateField(
        default=timezone.now,
        help_text="Fecha representativa para el Documento"
    )
    titulo = models.CharField(
        'Título',
        max_length=255,
        null=True,
        help_text="Título del documento"
    )
    tipo_documento = models.CharField(
        max_length=255,
        null=True,
        help_text="Tipo de Documento (Plano, Informe, etc)"
    )
    tipo_obra = models.CharField(
        max_length=255,
        null=True,
        help_text="Tipo de obra que representa el Documento (Civil, Mecánico, etc)"
    )
    revision = models.CharField(
        'Revisión',
        max_length=3,
        null=False,
        default='A',
        help_text="Revisión actual del Documento"
    )
    descripcion = models.CharField(
        'Descripción',
        max_length=1000,
        null=True,
        help_text="Breve descripción del Documento"
    )
    propietario = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        help_text="Miembro del equipo de trabajo responsable del Documento"
    )
    proyecto = models.ForeignKey(
        'Proyecto',
        related_name='documentos_proyecto',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="Proyecto al que pertenece el Documento"
    )
    reemplaza_a = models.ForeignKey(
        'self',
        related_name='documento_reemplazado_por',
        default=None,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        help_text="Documento al cual revisiona"
    )
    # reemplazado_por = models.ForeignKey(
    #     'self',
    #     related_name='docreemplazado_por',
    #     default=None,
    #     blank=True,
    #     null=True,
    #     on_delete=models.SET_NULL,
    #     help_text="Documento por el cual es revisionado"
    # )
    refiere_a = models.ManyToManyField(
        'self',
        blank=True,
        related_name='documentos_refiere_a',
        symmetrical=False,
        help_text="Documentos a los que hace referencia este Documento"
    )
    compuesto_por = models.ManyToManyField(
        'Archivo',
        blank=True,
        related_name='archivos',
        help_text="Archivos que componen el Documento"
    )

    class Meta:
        indexes = [
            models.Index(fields=['numero', 'revision']),
        ]
        ordering = ['numero', 'revision']
        permissions = (
            ('list_documentos', 'Can list documentos'),
            ('revision_documento', 'Add revision to Document'),
            # ("add_cheklist_document", "Add CheckList to Document"),
            # ("change_check_document", "Modify Checks to Document"),
            # ("add_revision_document", "Add Revision of a Document"),
            # ("delete_document_check", "Delete a Check Type to Document"),
            # ("add_document_check", "Add a Check Type to Document"),
            # ("change_document_check", "Modify the Check Types asign to Document"),
        )

    def __str__(self):
        """
        Cadena que representa a la instancia particular del modelo
        (p. ej. en el sitio de Administración)
        """
        return self.numero + ' (' + self.revision + ')'

    def revision_inc(self):
        """
        Retorna un valor de revisión válido incrementeando actual_rev
        """
        actual_rev = self.revision
        str_salida = ''
        band = True

        if actual_rev.isnumeric():
            str_salida = f'{int(actual_rev) + 1}'
            str_salida = str_salida[::-1]
        elif len(actual_rev) > 0:
            for char in actual_rev[::-1]:
                char_index = ascii_uppercase.find(char)
                if char_index >= 0:
                    if band:
                        if char == ascii_uppercase[-1]:
                            # Pongo actual en 'ascii_uppercase[0]'
                            str_salida = str_salida + ascii_uppercase[0]
                            # Pongo la bandera en True
                            band = True
                        else:
                            # Solo incremento
                            str_salida = str_salida + ascii_uppercase[char_index + 1]
                            band = False
                    else:
                        str_salida = str_salida + char

            if band:
                str_salida = str_salida + ascii_uppercase[0]
        else:
            str_salida = 'A'

        self.revision = str_salida[::-1]

    def make_revision_doc(self):
        """
        A partir del documento (self) retorna un documento que es una revisión de self
        """
        new_doc = Documento()
        new_doc.numero = self.numero
        new_doc.tipo = self.tipo
        new_doc.tipo_obra = self.tipo_obra
        new_doc.descripcion = self.descripcion
        new_doc.propietario = self.propietario
        new_doc.proyecto = self.proyecto
        new_doc.reemplaza_a = self
        new_doc.reemplazado_por = None
        new_doc.revision = self.revision
        new_doc.revision_inc()
        return new_doc

    def is_replaced(self):
        """
        Retorna True si el Documento fue reemplazado
        """
        return self.documento_reemplazado_por is None

    def is_replaces_to(self):
        """
        Retorna True si el Documento reemplaza a otro Documento
        """
        return self.reemplaza_a is not None

    # def document_rev(self, old_document):
    #     """
    #     A partir de un objeto Documento vacío, completa las propiedades
    #     de manera tal que se considere una revisión de old_document
    #     """
    #     self = copy(old_document)
    #     self.numero = old_document.numero
    #     self.propietario = old_document.propietario
    #     self.proyecto = old_document.proyecto
    #     self.tipo = old_document.tipo
    #     self.tipo_obra = old_document.tipo_obra
    #     self.descripcion = old_document.descripcion
    #     self.nombre_archivo = old_document.nombre_archivo
    #     self.directorio = old_document.directorio
    #     self.revision = old_document.revision
    #     self.revision.revision_inc()
    #     self.reemplaza_a = old_document


class Archivo(models.Model):
    """
    Modelo que define un archivo, parte de un documento (cad de planta, de vistas, etc)
    con sus características generales.
    """
    nombre_archivo = models.CharField(
        max_length=255,
        null=False,
        help_text="Nombre del archivo"
    )
    directorio = models.CharField(
        max_length=1000,
        null=False,
        help_text="Directorio de almacenamiento del archivo"
    )
    tipo_representacion = models.CharField(
        'Tipo de representación',
        max_length=255,
        null=True,
        help_text="Tipo de de representación del archivo (Planta, Modelo, Vista, etc)"
    )
    revision = models.CharField(
        'Revisión',
        max_length=3,
        null=False,
        default='A',
        help_text="Revisión actual del archivo"
    )
    descripcion = models.CharField(
        'Descripción',
        max_length=1000,
        null=True,
        help_text="Breve descripción del archivo"
    )
    fecha_creacion = models.DateField(
        'Fecha creación',
        default=timezone.now,
        help_text="Fecha de creación del archivo según el file system"
    )
    fecha_edicion = models.DateField(
        'Fecha edición',
        default=timezone.now,
        help_text="Fecha de edición del archivo según el file system"
    )
    reemplaza_a = models.ForeignKey(
        'self',
        related_name='archivo_reemplazado_por',
        default=None,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        help_text="Archivo al cual revisiona"
    )
    # reemplazado_por = models.ForeignKey(
    #     'self',
    #     related_name='%(class)s_reemplazado_por',
    #     default=None,
    #     blank=True,
    #     null=True,
    #     on_delete=models.CASCADE,
    #     help_text="Archivo por el cual es revisionado"
    # )
    proyecto = models.ForeignKey(
        'Proyecto',
        related_name='archivos_proyecto',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="Proyecto al que pertenece el Archivo"
    )
    propietario = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        help_text="Miembro del equipo de trabajo responsable del Archivo"
    )
    hash_archivo = models.IntegerField(
        default=None,
        null=True,
    )

    class Meta:
        indexes = [
            models.Index(fields=['nombre_archivo', 'revision']),
        ]
        ordering = ['nombre_archivo', 'revision']
        permissions = (
            ("list_archivos", "Can list Archivos"),
            ("revision_archivo", "Add a revision to Archivo"),
            # ("change_check_document", "Modify Checks to Document"),
            # ("add_revision_document", "Add Revision of a Document"),
            # ("delete_document_check", "Delete a Check Type to Document"),
            # ("add_document_check", "Add a Check Type to Document"),
            # ("change_document_check", "Modify the Check Types asign to Document"),
        )

    def __str__(self):
        """
        Cadena que representa a la instancia particular del modelo
        (p. ej. en el sitio de Administración)
        """
        return self.nombre_archivo + ' (' + self.revision + ')'

    def is_replaced(self):
        """
        Retorna True si el Archivo fue reemplazado
        """
        return self.archivo_reemplazado_por is None
