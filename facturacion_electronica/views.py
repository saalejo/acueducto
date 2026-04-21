from django.shortcuts import render

from .helpers import facturar, proceso_completo
from .models import Factura

def facturacion_electronica(request):
    facturas = Factura.objects.order_by('consecutivo')
    context = { 'facturas': facturas }
    return render(request, 'facturacion.html', context)

def facturar_todo(request):
    proceso_completo()

def facturar_por_id(request, factura_id):
    facturar(factura_id)
