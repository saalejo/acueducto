from reportlab.pdfgen import canvas
import io
from facturacion_electronica.constants import FORMAS_PAGO, MEDIOS_PAGO, UNIDADES, ESPECIAL_ELEMENTS, QR_CODE_SIZE, MESES, MESES_CONSUMO, REGIMENES
from facturacion_electronica.models import Factura
from util.helpers import anoMes, lecturas
from util.models import Cliente, Consumo, Control, Dispositivo, Elemento, Lectura, Movimiento, Ruta, Subsidio
import untangle
import base64
from django.http import FileResponse
import xlrd
from reportlab.graphics.barcode import code128
from reportlab_qrcode import QRCodeImage
from reportlab.lib.units import mm
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib.colors import PCMYKColor


def extractTotal(invoice):
    return {
        "base": invoice.cbc_LineExtensionAmount.cdata,
        "impuestos": invoice.cbc_TaxExclusiveAmount.cdata,
        "retenciones": invoice.cbc_ChargeTotalAmount.cdata,
        "descuentos": invoice.cbc_AllowanceTotalAmount.cdata,
        "total": invoice.cbc_PayableAmount.cdata,
    }


def extractLines(lines):
    return list(map(
        lambda x: {
            "id": x.cbc_ID.cdata,
            "unidad": UNIDADES[x.cbc_InvoicedQuantity["unitCode"]],
            "cantidad": x.cbc_InvoicedQuantity.cdata,
            "valor_unitario": x.cac_Price.cbc_PriceAmount.cdata,
            "sub_total": x.cbc_LineExtensionAmount.cdata,
            "iva": x.cac_TaxTotal.cbc_TaxAmount.cdata,
            "total": x.cbc_LineExtensionAmount.cdata,
            "descripcion": x.cac_Item.cbc_Description.cdata,
            "codigo": x.cac_Item.cac_StandardItemIdentification.cbc_ID.cdata
        },
        lines
    ))


def extractXMLData(factura):
    fact_xml = base64.b64decode(factura.resp_dian["invoicexml"]).decode('utf-8')
    obj = untangle.parse(fact_xml)
    emisor = obj.Invoice.cac_AccountingSupplierParty.cac_Party
    entidad = emisor.cac_PartyLegalEntity
    receptor = obj.Invoice.cac_AccountingCustomerParty.cac_Party
    cliente = receptor.cac_PartyLegalEntity
    contacto = emisor.cac_Contact
    ubicacion = emisor.cac_PhysicalLocation.cac_Address
    resolucion = obj.Invoice.ext_UBLExtensions.ext_UBLExtension[0].ext_ExtensionContent.sts_DianExtensions.sts_InvoiceControl
    medio_pago = obj.Invoice.cac_PaymentMeans.cbc_PaymentMeansCode
    forma_pago = obj.Invoice.cac_PaymentTerms.cbc_ReferenceEventCode
    return {
        "factura": {
            "consecutivo": obj.Invoice.cbc_ID.cdata,
            "cufe": obj.Invoice.cbc_UUID.cdata,
            "tipo_documento": obj.Invoice.cbc_ProfileID.cdata.replace("DIAN 2.1: ", ""),
            "fecha": obj.Invoice.cbc_IssueDate.cdata,
            "hora": obj.Invoice.cbc_IssueTime.cdata,
        },
        "empresa": {
            "nit": entidad.cbc_CompanyID.cdata,
            "nombre": entidad.cbc_RegistrationName.cdata,
            "telefono": contacto.cbc_Telephone.cdata,
            "correo": contacto.cbc_ElectronicMail.cdata,
            "zipcode": ubicacion.cbc_ID.cdata,
            "ciudad": ubicacion.cbc_CityName.cdata,
            "direccion": ubicacion.cac_AddressLine.cbc_Line.cdata
        },
        "cliente": {
            "nit": cliente.cbc_CompanyID.cdata,
            "nombre": cliente.cbc_RegistrationName.cdata,
            "telefono": contacto.cbc_Telephone.cdata,
            "correo": contacto.cbc_ElectronicMail.cdata,
            "zipcode": ubicacion.cbc_ID.cdata,
            "ciudad": ubicacion.cbc_CityName.cdata,
            "direccion": ubicacion.cac_AddressLine.cbc_Line.cdata,
            "regimen": obj.Invoice.cac_AccountingCustomerParty.cac_Party.cac_PartyTaxScheme.cbc_TaxLevelCode.cdata
        },
        "resolucion": {
            "resolucion": resolucion.sts_InvoiceAuthorization.cdata,
            "fecha_inicio": resolucion.sts_AuthorizationPeriod.cbc_StartDate.cdata,
            "fecha_fin": resolucion.sts_AuthorizationPeriod.cbc_EndDate.cdata,
            "prefijo": resolucion.sts_AuthorizedInvoices.sts_Prefix.cdata,
            "desde": resolucion.sts_AuthorizedInvoices.sts_From.cdata,
            "hasta": resolucion.sts_AuthorizedInvoices.sts_To.cdata
        },
        "pago": {
            "medio": MEDIOS_PAGO[medio_pago.cdata],
            "forma": FORMAS_PAGO[forma_pago.cdata]
        },
        "filas": extractLines(obj.Invoice.cac_InvoiceLine),
        "total": extractTotal(obj.Invoice.cac_LegalMonetaryTotal)
    }

def pintarConsumo(p, elementos, consumo): 
    d = Drawing(100, 100)
    valores = consumo.values_list(*MESES_CONSUMO).first()
    bar = VerticalBarChart()
    elemento = elementos.get(nombre="consumos")
    bar.x, bar.y = elemento.x, elemento.y
    bar.categoryAxis.categoryNames = MESES
    bar.data = [[eval(i) for i in [*valores]]]
    bar.bars[0].fillColor   = PCMYKColor(45, 0, 20, 0, alpha=85)
    d.add(bar)
    d.drawOn(p, elemento.x, elemento.y)
    return consumo


def pintarElementos(p, elementos, context, cliente):
    for elemento in elementos:
        if elemento.nombre not in ESPECIAL_ELEMENTS:
            try:
                texto = eval(elemento.formula)
            except Exception as e:
                print(elemento.nombre)
                print(e)
                texto = ''
            p.setFont(elemento.font, elemento.size)
            p.drawRightString(elemento.x, elemento.y, str(texto))
    
def pintarFilas(p, elementos, context):
    elemento = elementos.get(nombre="factura_conceptos")
    avance = 0
    avance_x = 20
    p.setFont(elemento.font, elemento.size)
    for fila in context["filas"]:
        p.drawString(elemento.x, elemento.y + avance, fila["codigo"])
        p.drawString(elemento.x + avance_x*3, elemento.y + avance, fila["descripcion"])
        p.drawString(elemento.x + avance_x*14, elemento.y + avance, fila["unidad"])
        p.drawString(elemento.x + avance_x*17, elemento.y + avance, '{:,}'.format(int(float(fila["valor_unitario"]))))
        p.drawString(elemento.x + avance_x*20, elemento.y + avance, '{:,}'.format(int(float(fila["cantidad"]))))
        p.drawString(elemento.x + avance_x*21, elemento.y + avance, '{:,}'.format(int(float(fila["sub_total"]))))
        p.drawString(elemento.x + avance_x*23, elemento.y + avance, '{:,}'.format(int(float(fila["iva"]))))
        p.drawString(elemento.x + avance_x*25, elemento.y + avance, '{:,}'.format(int(float(fila["total"]))))
        avance += 20
    
def pintarQR(p, elementos, context):
    mensaje = f"""
    NumFac: {context["factura"]["consecutivo"]}
    FecFac: {context["factura"]["fecha"]} 
    NitFac: {context["empresa"]["nit"]}
    DocAdq: {context["cliente"]["nit"]}
    ValFac: {context["total"]["base"]}
    ValIva: {context["total"]["impuestos"]}
    ValOtroIm: {context["total"]["impuestos"]}
    ValTotal: {context["total"]["total"]}
    CUFE: {context["factura"]["cufe"]}
    """
    elemento = elementos.get(nombre="qr_code")
    qr = QRCodeImage(mensaje, size=QR_CODE_SIZE * mm)
    qr.drawOn(p, elemento.x, elemento.y)
    
def pintarBarCode(p, elementos, context):
    codigo = "7707246813579"
    fecha = context["factura"]["fecha"].replace("-", "")
    consecutivo = context["factura"]["consecutivo"]
    valor = context["total"]["total"].replace(".00", "").zfill(10)
    mensaje = f"(415){codigo}(8020){consecutivo}(3900){valor}(96){fecha}"
    elemento = elementos.get(nombre="bar_code")
    barcode = code128.Code128(mensaje,barHeight=20*mm, barWidth=.5)
    barcode.drawOn(p, elemento.x, elemento.y)
    p.drawString(elemento.x + 15, elemento.y - 10, mensaje)

def pintarGrupo(p, elemento, grupo, avance_x=60, avance_y=15):
    for index, key in enumerate(grupo.keys()):
        p.drawString(elemento.x-avance_x, elemento.y+(avance_y*(index -1)), key)
    for index, value in enumerate(grupo.values()):
        p.drawRightString(elemento.x+avance_x, elemento.y+(avance_y*(index -1)), value)

def pintarLecturas(p, elementos, movimiento, consumo):
    lecturas(movimiento, consumo, comparar_fechas=False)
    elemento = elementos.get(nombre="consumo_lecturas")
    p.setFont(elemento.font, elemento.size)
    consumo_periodo = consumo.lecturaActual - consumo.lecturaAnterior
    grupo = {
        "Lectura anterior:": str(consumo.lecturaAnterior),
        "Lectura actual:": str(consumo.lecturaActual),
        "Consumo m3:": str(consumo_periodo),
        "Hasta:": str(consumo.desde),
        "Desde:": str(consumo.hasta),
    }
    pintarGrupo(p, elemento, grupo)


def pintarTotales(p, elementos, context):
    elemento = elementos.get(nombre="factura_totales")
    p.setFont(elemento.font, elemento.size)
    grupo = {
        "Total factura electronica:": context['total']['total'],
        "Descuentos:": context['total']['descuentos'],
        "Retenciones:": context['total']['retenciones'],
        "Impuestos:": context['total']['impuestos'],
        "Base:": context['total']['base'],
    }
    pintarGrupo(p, elemento, grupo, avance_x=100)


def generarPdf(factura_id):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    elementos = Elemento.objects.all()
    factura = Factura.objects.get(pk=factura_id)
    context = extractXMLData(factura)
    movimiento = Movimiento.objects.get(docref=factura.prefactura)
    cliente = Cliente.objects.get(codcte=movimiento.nitcte)
    fecha = xlrd.xldate_as_datetime(float(movimiento.fecmvt), 0).date()
    movimiento.fecmvt = fecha.strftime("%Y/%m/%d")
    ano, _, _ = anoMes(movimiento.fecmvt)
    consumo = Consumo.objects.filter(codcte=movimiento.nitcte, feccon__contains=ano)
    pintarElementos(p, elementos, context, cliente)
    pintarFilas(p, elementos, context)
    pintarQR(p, elementos, context)
    pintarBarCode(p, elementos, context)
    pintarConsumo(p, elementos, consumo)
    pintarLecturas(p, elementos, movimiento, consumo.first())
    pintarTotales(p, elementos, context)
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer
    