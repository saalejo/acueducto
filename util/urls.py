from django.urls import path

from util.viewsets import *
from .views import exportar, inicio
from django.urls import path, include
from rest_framework import routers

app_name = 'util'

router = routers.DefaultRouter()
router.register(r'lecturas', LecturaViewSet)
router.register(r'rutas', RutaViewSet)

urlpatterns =[
    path('', include(router.urls)),
    path('upload', inicio, name='inicio'),
    path('generar_ruta/', GenerarRutaView.as_view(), name='generar_ruta'),
    path('guardar_ruta/', GuardarRutaView.as_view(), name='generar_ruta'),
    path('ruta_simple/', RutaList.as_view(), name='ruta_simple'),
    path('exportar', exportar, name='exportar_todo'),
    path('exportar/<str:fecha>', exportar, name='exportar'),
]

# http://localhost:8000/exportar/2021-10-31