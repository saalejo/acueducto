from django.urls import path
from .views import exportar, inicio

app_name = 'util'

urlpatterns =[
    path('', inicio, name='inicio'),
    path('exportar', exportar, name='exportar_todo'),
    path('exportar/<str:fecha>', exportar, name='exportar'),
]

# http://localhost:8000/exportar/2021-10-31