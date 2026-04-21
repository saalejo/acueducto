import requests
from django.template.loader import render_to_string
import json

import base64
from facturacion_electronica.models import Apidian, Entidad, Factura, Fila, Resolucion
from util.models import Cliente, Movimiento
from .constants import *

from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMessage
import zipfile36 as zipfile
import pathlib
import re


def obtener_numero(valor):
    return valor.split(".")[0]


def obtener_consecutivo():
    resolucion = Resolucion.objects.filter(activa=True).first()
    resolucion.consecutivo += 1
    resolucion.save()
    return resolucion.consecutivo
    
    
def obtener_entidad(informacion):
    cliente = Cliente.objects.filter(codcte=informacion.nitcte).first()
    if cliente:
        entidad, _ = Entidad.objects.get_or_create(identificacion=cliente.nitcte)
        entidad.nombre = cliente.nomcte
        entidad.telefono = cliente.telcte
        entidad.email = cliente.correo
        entidad.direccion = VEREDA
        entidad.registroMercantil = REGISTRO_MERCANTIL_DEFAULT
        entidad.tipoIdentificacion = CEDULA_DE_CIUDADANIA
        entidad.tipoOrganizacion = PERSONA_NATURAL
        entidad.ciudad = EL_CARMEN_DE_VIBORAL
        entidad.regimen = NO_RESPONSABLE_DE_IVA
        entidad.save()
        return entidad


def obtener_factura(entidad, informacion):
    factura = Factura()
    factura.prefactura = informacion.docref
    factura.entidad_id = entidad.pk
    factura.formaPago = CONTADO
    factura.metodoPago = EFECTIVO
    factura.plazo = PLAZO
    factura.sumDescuentos = CERO
    factura.consecutivo = obtener_consecutivo()
    factura.total = obtener_numero(informacion.debito)
    factura.totalPagar = factura.total
    factura.save()
    return factura


def definir_conceptos(factura, filas):
    for filap in filas:
        fila = Fila()
        fila.factura_id = factura.pk 
        fila.descripcion = filap.desmvt
        fila.unidad_de_medida_cod = METRO_CUBICO
        fila.cantidad = UNA_UNIDAD
        fila.importe = obtener_numero(filap.credito)
        fila.valorUnitario = obtener_numero(filap.credito)
        fila.save()
    
def crear_factura(movimientos):
    informacion = movimientos.filter(credito="0.0").first()
    filas = movimientos.filter(debito="0.0").all()
    entidad = obtener_entidad(informacion)
    if entidad:
        factura = obtener_factura(entidad, informacion)
        definir_conceptos(factura, filas)
        return factura
        


def preparar_factura_electronica(factura):
    try:
        data = render_to_string(
            'facturacion_electronica/factura.json', {'factura': factura})
        factura.fe_json = json.loads(data)
        factura.es_valida = True      
        factura.save()            
        return True
    except Exception as e:
        return False
    
def facturacion_electronica(factura):
    preparar_factura_electronica(factura)
    try:
        apidian = Apidian.objects.first()
        response = requests.post(
            f"{apidian.url}/ubl2.1/invoice/{apidian.token_dian}",
            headers = {
                "Authorization": f"Bearer {apidian.token_api}",
                "Accept": "application/json"
            },
            json = factura.fe_json
        )
        factura.resp_dian = response.json()
        try:
            factura.cufe = factura.resp_dian.get('cufe', None)
            factura.zip_code = factura.resp_dian.get('ResponseDian').get('Envelope').get('Body').get('SendTestSetAsyncResponse').get('SendTestSetAsyncResult').get('ZipKey')
        except Exception as e:
            print("Problem getting cufe")
            print(e)
        factura.save()          
        return True
    except Exception as e:
        print("Problem getting response")
        print(e)
        return False

def notaElectronica(documento, naturaleza):
    try:
        if documento.factura.empresa.es_facturador_e: 
            factura = documento.factura
            response = requests.post(
                'https://apidian.agapanto.com.co/api/ubl2.1/'+naturaleza+'-note/' + factura.empresa.fe_token_dian,
                headers = {
                    'Authorization': 'Bearer ' + factura.empresa.fe_token_api,
                    'Accept': 'application/json'
                },
                json = documento.json
            )
            documento.resp_dian = response.json()
            try:
                documento.cude = documento.resp_dian.get('cude', None)
                documento.zip_code = documento.resp_dian.get('ResponseDian').get(
                    'Envelope').get('Body').get('SendTestSetAsyncResult').get('ZipKey')
            except Exception as e:
                print(e)
            documento.save()
    except Exception as e:
        print(e)



def preparar_facturas():
    rechazadas = []
    rechazadas_dian = []
    movimientos = Movimiento.objects.filter(facturado=False).exclude(desmvt="A N U L A D A")
    grupos = movimientos.order_by('numcom').values('numcom').distinct()
    for grupo in grupos:
        movimientos_grupo = movimientos.filter(numcom=grupo['numcom'])
        factura = crear_factura(movimientos_grupo)
        if factura:
            if preparar_factura_electronica(factura):
                movimientos_grupo.update(facturado=True, factura_id=factura.pk)
            else:
                rechazadas_dian += [{ "movimiento": grupo['numcom'], "factura": factura.pk }]
        else:
            rechazadas += [grupo['numcom']]
    return rechazadas, rechazadas_dian
    
    
def facturar(factura_id):
    factura = Factura.objects.get(pk=factura_id)
    facturacion_electronica(factura)
    consultar(factura)
    notify_mailtrap(factura)
    



def consultar(factura):
    try:
        apidian = Apidian.objects.first()
        response = requests.post(
            f"{apidian.url}/statuszip",
            headers = { "Accept": "application/json" },
            json = {
                "zipkey": factura.zip_code,
                "ambiente": apidian.ambiente,
                "certificate": apidian.certificate,
                "password": apidian.password
            }
        )
        return response
    except Exception as e:
        print("Problem getting response")
        print(e)
        return False 
    


def compress(resp_dian):
    pathlib.Path('tmp').mkdir(parents=True, exist_ok=True) 
    zipPath = "tmp/factura.zip"
    with zipfile.ZipFile(zipPath, 'w') as zipFile:
        zipFile.writestr(resp_dian["urlinvoicexml"], base64.b64decode(resp_dian["invoicexml"]))
    return f"{zipPath}"
    

def notify_mailtrap(factura):
    apidian = Apidian.objects.first()
    message = render_to_string("email.html", {"factura": factura})
    email = EmailMessage(
        subject=settings.EMAIL_SUBJECT.format(factura.fe_json['number']),
        body=message,
        from_email=settings.EMAIL_FROM,
        to=[factura.entidad.email],
        cc=[settings.EMAIL_CC]
    )
    email.content_subtype = "html"
    base_url = f"{apidian.url}/download/{apidian.nit}"
    file_name_pdf = f"{factura.resp_dian['urlinvoicepdf']}"
    file_name_zip = file_name_pdf.replace('.pdf', '.zip')
    file_pdf = requests.get(f"{base_url}/{file_name_pdf}")
    file_zip = requests.get(f"{base_url}/{file_name_zip}")
    email.attach(file_name_pdf, file_pdf.content, file_pdf.headers["Content-Type"])
    email.attach(file_name_zip, file_zip.content, file_zip.headers["Content-Type"])
    email.send()


def notify_mailtrap_by_id(factura_id):
    factura = Factura.objects.get(pk=factura_id)
    notify_mailtrap(factura)


def proceso_completo():
    facturas = Factura.objects.filter(zip_code=None)
    for factura in facturas:
        facturacion_electronica(factura)
    for factura in facturas:
        consultar(factura)
        notify_mailtrap(factura)