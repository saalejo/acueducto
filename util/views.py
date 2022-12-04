from django.shortcuts import render
from tablib import Dataset
from util.helpers import generarDocumento, importarDocumento
from util.models import Elemento, Subsidio
from util.resources import ConsumoResource, ControlResource, MovimientoResource, SubsidioResource

documentos = [
    ('control', ControlResource()),
    ('consumo', ConsumoResource()),
    ('movimiento', MovimientoResource()),
    ('subsidio', SubsidioResource()),
]

def inicio(request):   
    if request.method == 'POST' :
        for clave, valor in documentos:
            if clave in request.FILES:
                importarDocumento(
                    request.FILES[clave],
                    valor
                )
    return render(request, 'inicio.html', {}) 

def exportar(request):
    elementos = Elemento.objects.all()
    return generarDocumento(elementos)