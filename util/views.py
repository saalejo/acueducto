from django.shortcuts import render
from util.helpers import generarDocumento, importarDocumento
from util.resources import ConsumoResource, ControlResource, MovimientoResource, SubsidioResource, ClienteResource

documentos = [
    ('control', ControlResource()),
    ('consumo', ConsumoResource()),
    ('movimiento', MovimientoResource()),
    ('subsidio', SubsidioResource()),
    ('cliente', ClienteResource()),
]

def inicio(request):   
    errores = []
    if request.method == 'POST':
        for clave, valor in documentos:
            print('************' + clave)
            if clave in request.FILES and request.FILES[clave] != None:
                print('+++++++++++++++' + clave)
                errores.append({
                    'documento': clave,
                    'errores': importarDocumento(request.FILES[clave], valor)
                })
    context = { 'mensaje': 'Documentos importados con exito', 'errores': errores }
    return render(request, 'inicio.html', context)

def exportar(request, fecha=None):
    return generarDocumento(fecha)

def exportarConsumos(request):
    dataset = ConsumoResource().export()
    
