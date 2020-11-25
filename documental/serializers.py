from rest_framework import serializers
from .models import Documento

class DocumentoSerializer(serializers.ModelSerializer):
    """
    ---
    """
    proyecto = serializers.StringRelatedField()
    reemplaza_a = serializers.StringRelatedField()
    propietario = serializers.StringRelatedField()

    class Meta:
        model = Documento
        fields = [
            'pk',
            'numero',
            'fecha',
            'titulo',
            'tipo_documento',
            'tipo_obra',
            'revision',
            'descripcion',
            'propietario',
            'proyecto',
            'reemplaza_a',
        ]
