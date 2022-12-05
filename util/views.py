from django.shortcuts import render
from util.helpers import generarDocumento, importarDocumento
from util.resources import ConsumoResource, ControlResource, MovimientoResource, SubsidioResource

documentos = [
    ('control', ControlResource()),
    ('consumo', ConsumoResource()),
    ('movimiento', MovimientoResource()),
    ('subsidio', SubsidioResource()),
]

def inicio(request):   
    if request.method == 'POST':
        for clave, valor in documentos:
            if clave in request.FILES and request.FILES[clave] != None:
                importarDocumento(request.FILES[clave], valor)
    context = { 'mensaje': 'Documentos importados con exito' }
    return render(request, 'inicio.html', context) 

def exportar(request, fecha=None):
    return generarDocumento(fecha)