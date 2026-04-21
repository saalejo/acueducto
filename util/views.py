from django.shortcuts import render
from facturacion_electronica.helpers import preparar_facturas
from util.helpers import generarDocumento, importarDocumento
from util.resources import ConsumoResource, ControlResource, MovimientoResource, SubsidioResource, ClienteResource
from django.shortcuts import redirect

documentos = [
    ('control', ControlResource()),
    ('consumo', ConsumoResource()),
    ('movimiento', MovimientoResource()),
    ('subsidio', SubsidioResource()),
    ('cliente', ClienteResource()),
]

def inicio(request):
    return redirect("/static/spa/index.html")

def upload(request):   
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
    if not len(errores):
        rechazadas, rechazadas_dian = preparar_facturas()
        errores.append({
            'documento': "rechazadas app",
            'errores': rechazadas
        })
        errores.append({
            'documento': "rechazadas dian",
            'errores': rechazadas_dian
        })
    return render(request, 'inicio.html', context)

def exportar(request, fecha=None):
    return generarDocumento(fecha)

def exportarConsumos(request):
    dataset = ConsumoResource().export()
    
