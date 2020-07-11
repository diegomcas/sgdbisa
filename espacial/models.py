from django.contrib.gis.db import models


# Create your models here.
class ElementoEspacial(models.Model):
    PUNTOS = 'PT'
    POLIGONO = 'PL'
    LINEA = 'LN'
    TIPO_ELEMENTO_CHOICES = [
        (PUNTOS, 'Puntos'),
        (POLIGONO, 'Poligono'),
        (LINEA, 'Linea'),
    ]

    tipo_elemento = models.CharField(
        max_length=2,
        choices=TIPO_ELEMENTO_CHOICES,
        default=POLIGONO,
    )
    punto = models.PointField(
        null=True
    )
    poligono = models.PolygonField(
        null=True
    )
    linea = models.LineStringField(
        null=True
    )
    atributo = models.CharField(
        max_length=255,
        null=True,
        help_text="Atributo del punto."
    )

    def __str__(self):
        return self.tipo_elemento
