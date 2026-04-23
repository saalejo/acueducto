import io
import os
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from facturacion_electronica.helpers import preparar_facturas
from util.helpers import generarDocumento, importarDocumento
from util.resources import ConsumoResource, ControlResource, MovimientoResource, SubsidioResource, ClienteResource

_DRIVE_SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def _load_credentials():
    token_file = settings.GOOGLE_TOKEN_FILE
    if not os.path.exists(token_file):
        return None
    creds = Credentials.from_authorized_user_file(token_file, _DRIVE_SCOPES)
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(token_file, 'w') as f:
            f.write(creds.to_json())
    return creds if creds and creds.valid else None

def _drive_service():
    creds = _load_credentials()
    if creds is None:
        raise RuntimeError('Google Drive no autorizado. Visita /google-auth/ para autorizar.')
    return build('drive', 'v3', credentials=creds)

def _oauth_flow():
    client_config = {
        'web': {
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_CLIENT_SECRET,
            'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
            'token_uri': 'https://oauth2.googleapis.com/token',
            'redirect_uris': [settings.GOOGLE_REDIRECT_URI],
        }
    }
    return Flow.from_client_config(client_config, scopes=_DRIVE_SCOPES,
                                   redirect_uri=settings.GOOGLE_REDIRECT_URI)

def google_auth(request):
    flow = _oauth_flow()
    auth_url, _ = flow.authorization_url(access_type='offline', prompt='consent')
    return redirect(auth_url)

def google_auth_callback(request):
    flow = _oauth_flow()
    flow.fetch_token(authorization_response=request.build_absolute_uri())
    creds = flow.credentials
    with open(settings.GOOGLE_TOKEN_FILE, 'w') as f:
        f.write(creds.to_json())
    return redirect('util:consultar_factura')

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

def consultar_factura(request):
    codigo = request.GET.get('codigo', '').strip()
    context = {'codigo': codigo}
    if codigo:
        try:
            service = _drive_service()
            folder_id = settings.GOOGLE_DRIVE_FOLDER_ID
            padded = codigo.zfill(6)
            query = f"name contains '{padded}-' and mimeType='application/pdf' and trashed=false"
            if folder_id:
                query += f" and '{folder_id}' in parents"
            result = service.files().list(
                q=query,
                fields='files(id, name)',
                orderBy='name desc',
                pageSize=1,
                includeItemsFromAllDrives=True,
                supportsAllDrives=True,
            ).execute()
            files = result.get('files', [])
            if files:
                context['file_id'] = files[0]['id']
                context['file_name'] = files[0]['name']
            else:
                context['error'] = f'No se encontró ningún archivo con el código "{codigo}".'
        except Exception as e:
            context['error'] = f'Error al buscar en Google Drive: {e}'
    return render(request, 'consultar_factura.html', context)


def proxy_pdf(request, file_id):
    try:
        service = _drive_service()
        media_request = service.files().get_media(fileId=file_id, supportsAllDrives=True)
        buf = io.BytesIO()
        downloader = MediaIoBaseDownload(buf, media_request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
        buf.seek(0)
        disposition = 'attachment' if request.GET.get('download') else 'inline'
        file_name = request.GET.get('nombre', 'factura.pdf')
        response = HttpResponse(buf.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'{disposition}; filename="{file_name}"'
        response['X-Frame-Options'] = 'SAMEORIGIN'
        return response
    except Exception as e:
        return HttpResponse(f'Error al obtener el archivo: {e}', status=500)


def exportarConsumos(request):
    dataset = ConsumoResource().export()
    
