from rest_framework import serializers

from util.models import *

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['codcte', 'nomcte', 'telcte', 'estrato']
        
class ConsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumo
        fields = [
            'lecant',
            'sector',
            'feccon',
            'ruta',
            'conenero',
            'confebrero',
            'conmarzo',
            'conabril',
            'conmayo',
            'conjunio',
            'conjulio',
            'conagosto',
            'conseptiem',
            'conoctubre',
            'connoviemb',
            'condiciemb',
        ]
        
class LecturaSerializer(serializers.ModelSerializer):
    consumo = ConsumoSerializer()
    cliente = ClienteSerializer()
    class Meta:
        model = Lectura
        exclude = ['fecha']
        
class RutaSerializer(serializers.ModelSerializer):
    lecturas = LecturaSerializer(many=True, read_only=True)
    class Meta:
        model = Ruta
        fields = '__all__'

class RutaSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ruta
        fields = ['id', 'vereda', 'estado', 'fecha']