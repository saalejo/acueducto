from django.urls import path

from util.viewsets import LecturaViewSet
from .views import exportar, inicio
from django.urls import path, include
from rest_framework import routers

app_name = 'util'

router = routers.DefaultRouter()
router.register(r'lecturas', LecturaViewSet)

urlpatterns =[
    path('', include(router.urls)),
    path('', inicio, name='inicio'),
    path('exportar', exportar, name='exportar_todo'),
    path('exportar/<str:fecha>', exportar, name='exportar'),
]

# http://localhost:8000/exportar/2021-10-31