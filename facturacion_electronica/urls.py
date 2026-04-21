from django.urls import path

from .views import facturacion_electronica, facturar, facturar_todo
from django.urls import path

app_name = 'facturacion_electronica'

urlpatterns =[
    path('', facturacion_electronica, name='facturacion_electronica'),
    path('facturar_todo', facturar_todo, name='facturar_todo'),
    path('facturar/<int:factura_id>', facturar, name='facturar'),
]