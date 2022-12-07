from tablib import Dataset
import reportlab
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

from util.models import Consumo, Control, Elemento, Movimiento, Subsidio
from .numero_letras import *

meses = [
    'enero',
    'febrero',
    'marzo',
    'abril',
    'mayo',
    'junio',
    'julio',
    'agosto',
    'septiembre',
    'octubre',
    'noviembre',
    'diciembre',
]

meses30 = [11, 4, 6, 8]
meses31 = [1, 3, 5, 7, 9, 10, 12]

def importarDocumento(archivo, resource):
    dataset = Dataset()
    dataset.load(archivo.read())
    result = resource.import_data(dataset, dry_run=True)
    if not result.has_errors():
        resource.import_data(dataset, dry_run=False)

def anoMes(fecha):
    ano = fecha[:4]
    mes = int(fecha[5:7])
    mesNombre = meses[mes-2]
    mesAnterior = meses[mes-3]
    return ano, mesNombre, mesAnterior

def lecturas(subsidio, consumo):
    consumo.lecturaActual = 0
    consumo.lecturaAnterior = 0
    anoSubsidio, mesSubsidio, mesAnteriorSubsidio = anoMes(subsidio.fecmvt)
    anoConsumo, mesConsumo, mesAnteriorConsumo = anoMes(consumo.feccon)
    if anoSubsidio == anoConsumo and subsidio.fecmvt <= consumo.feccon:        
        lecturaActual = getattr(consumo, mesSubsidio)
        lecturaAnterior = getattr(consumo, mesAnteriorSubsidio)
        consumo.lecturaActual = int(float(lecturaActual))
        consumo.lecturaAnterior = int(float(lecturaAnterior))
        mes = int(subsidio.fecmvt[5:7])
        if mes > 1:
            anterior =  mes - 1
        else:
            anterior =  12
        diaFin = '31' if anterior in meses31 else '30' if anterior in meses30 else '28'
        consumo.desde = f'{anoSubsidio}-{anterior}-01'
        consumo.hasta = f'{anoSubsidio}-{anterior}-{ diaFin }'

def generarDocumento(fecha):
    movimientosNombre = 'Movimientos'
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    elementos = Elemento.objects.all()
    if fecha:
        subsidios = Subsidio.objects.filter(fecmvt__contains=fecha)
    else:
        subsidios = Subsidio.objects.all()
    control = Control.objects.first()
    for subsidio in subsidios:
        for elemento in elementos:
            if elemento.nombre != movimientosNombre:
                anoSubsidio, mesSubsidio, mesAnteriorSubsidio = anoMes(subsidio.fecmvt)
                consumo = Consumo.objects.filter(codcte=subsidio.nitcte, feccon__contains=anoSubsidio).first()
                lecturas(subsidio, consumo)
                texto = eval(elemento.formula)
                p.drawString(elemento.x, elemento.y, str(texto))
        movimientos = Movimiento.objects.filter(numcom=subsidio.factura)
        elemento = elementos.get(nombre=movimientosNombre)
        avance = 0
        for movimiento in movimientos:
            if float(movimiento.debito) == 0 and float(movimiento.credito) > 0:
                p.drawString(elemento.x, elemento.y + avance, '{:,}'.format(int(float(movimiento.credito))))
                p.drawString(elemento.x + 50, elemento.y + avance, movimiento.desmvt)
                avance += 20
        p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='documentos.pdf')
