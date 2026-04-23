from django.urls import path

from util.viewsets import *
from .views import exportar, inicio, upload, consultar_factura, proxy_pdf, google_auth, google_auth_callback
from django.urls import path, include
from rest_framework import routers

app_name = 'util'

router = routers.DefaultRouter()
router.register(r'lecturas', LecturaViewSet)
router.register(r'rutas', RutaViewSet)

urlpatterns =[
    path('', inicio, name='inicio'),
    path('upload', upload, name='upload'),
    path('', include(router.urls)),
    path('generar_ruta/', GenerarRutaView.as_view(), name='generar_ruta'),
    path('guardar_ruta/', GuardarRutaView.as_view(), name='generar_ruta'),
    path('ruta_simple/', RutaList.as_view(), name='ruta_simple'),
    path('exportar', exportar, name='exportar_todo'),
    path('exportar/<str:fecha>', exportar, name='exportar'),
    path('consultar-factura/', consultar_factura, name='consultar_factura'),
    path('consultar-factura/pdf/<str:file_id>/', proxy_pdf, name='proxy_pdf'),
    path('google-auth/', google_auth, name='google_auth'),
    path('oauth2callback/', google_auth_callback, name='google_auth_callback'),
]

# http://localhost:8000/exportar/2021-10-31