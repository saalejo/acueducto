from rest_framework import viewsets
from util.models import Lectura
from util.serializers import LecturaSerializer

class LecturaViewSet(viewsets.ModelViewSet):
    queryset = Lectura.objects.all()
    serializer_class = LecturaSerializer
    filterset_fields = ['codigo']