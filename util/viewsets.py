
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework import viewsets
from util.helpers import crearRuta
from util.models import Lectura
from util.serializers import *

class LecturaViewSet(viewsets.ModelViewSet):
    queryset = Lectura.objects.all()
    serializer_class = LecturaSerializer

class RutaViewSet(viewsets.ModelViewSet):
    queryset = Ruta.objects.all()
    serializer_class = RutaSerializer

class GuardarRutaView(APIView):
    parser_classes = [JSONParser]
    
    def post(self, request, *args, **kwargs):
        request_json = request.data
        for l in request_json['lecturas']:
            lectura = Lectura.objects.get(pk=l['id'])
            lectura.lectura = l['lectura']
            lectura.save()
        if request_json['terminar']:
            Ruta.objects.filter(id=request_json['ruta_id']).update(
                estado='Terminada'
            )
        response = {'ruta_id': request_json['ruta_id'] }
        return JsonResponse(data=response, status=200)

class GenerarRutaView(APIView):
    parser_classes = [JSONParser]
    
    def post(self, request, *args, **kwargs):
        request_json = request.data
        element = crearRuta(
            request_json['dispositivo'],
            request_json['vereda']
        )
        response = {'ruta': element }
        return JsonResponse(data=response, status=200)

from rest_framework import generics
from rest_framework.permissions import IsAdminUser

class RutaList(generics.ListCreateAPIView):
    queryset = Ruta.objects.filter(estado='Activa').all()
    serializer_class = RutaSimpleSerializer
    filterset_fields = ['dispositivo__codigo']