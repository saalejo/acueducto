from django.urls import path
from .views import exportar, inicio

app_name = 'util'

urlpatterns =[
    path('', inicio, name='inicio'),
    path('exportar', exportar, name='exportar'),
]
