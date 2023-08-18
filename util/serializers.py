from rest_framework import serializers

from util.models import Lectura

class LecturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lectura
        fields = ['codigo', 'cliente', 'vereda', 'sector', 'ruta', 'lecturaAnterior', 'lectura', 'fecha_ruta']