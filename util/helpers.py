from tablib import Dataset
import reportlab
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

from util.models import Consumo, Movimiento, Subsidio

def importarDocumento(archivo, resource):
    dataset = Dataset()
    dataset.load(archivo.read())
    result = resource.import_data(dataset, dry_run=True)
    if not result.has_errors():
        resource.import_data(dataset, dry_run=False)

def generarDocumento(elementos):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    subsidios = Subsidio.objects.all()
    for subsidio in subsidios:
        for elemento in elementos:
            consumo = Consumo.objects.get(codcte=subsidio.nitcte)
            movimientos = Movimiento.objects.filter(numcom=subsidio.factura)
            texto = ''
            exec(elemento.formula)
            p.drawString(elemento.x, elemento.y, texto)
        p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='documentos.pdf')
