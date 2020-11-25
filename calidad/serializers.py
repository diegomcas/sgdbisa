from rest_framework import serializers
from .models import TipoChequeo, Chequeo
from documental.models import Documento

class TipoChequeoSerializer(serializers.ModelSerializer):
    """
    ---
    """
    class Meta:
        model = TipoChequeo
        fields = ['pk', 'nombre', 'ayuda']

class ChequeoSerializer(serializers.ModelSerializer):
    """
    ---
    """
    verificado_por = serializers.StringRelatedField()
    tipo_chequeo = TipoChequeoSerializer(read_only=True)

    class Meta:
        model = Chequeo
        fields = [
            'pk',
            'tipo_chequeo',
            'aplica',
            'verificado',
            'verificado_por',
        ]

class DocumentoChequeoSerializer(serializers.ModelSerializer):
    """
    ---
    """
    numero = serializers.StringRelatedField()
    propietario = serializers.StringRelatedField()
    chequeo_documento = ChequeoSerializer(many=True, read_only=True)

    class Meta:
        model = Documento
        fields = ['pk', 'numero', 'propietario', 'chequeo_documento']

class ChequeoRealizadoListSerializer(serializers.ListSerializer):
    """
    ---
    """
    def create(self, validated_data):
        print("Metodo create")

        print(f"validated_data= {validated_data}")

        owner = validated_data[1]['owner']

        ret = []
        for val_dt in validated_data:
            verif_by = val_dt.pop('verif_by', None)
            aplica = val_dt.pop('aplica', None)

            # Obtengo el objeto "Chequeo" desde la base de datos
            chequeo = Chequeo.objects.get(pk=val_dt['pk'])

            if aplica:
                if chequeo.verificado:
                    if val_dt['verificado']:
                        if verif_by != chequeo.verificado_por:
                            chequeo.verificado_por = owner
                    else:
                        chequeo.verificado = val_dt['verificado']
                        chequeo.verificado_por = None
                else:
                    if val_dt['verificado']:
                        chequeo.verificado = val_dt['verificado']
                        chequeo.verificado_por = owner
                chequeo.aplica = aplica
            else:
                chequeo.aplica = False
                chequeo.verificado = False
                chequeo.verificado_por = None

            ret.append(chequeo)

            chequeo.save()

        return ret

class ChequeoRealizadoSerializer(serializers.ModelSerializer):
    """
    ---
    """
    pk = serializers.IntegerField()
    verif_by = serializers.CharField(write_only=True, allow_null=True)

    class Meta:
        model = Chequeo
        fields = ['pk', 'aplica', 'verificado', 'verif_by']
        list_serializer_class = ChequeoRealizadoListSerializer
