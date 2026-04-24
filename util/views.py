import os
import threading
from django.conf import settings
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render, redirect
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import AuthorizedSession, Request
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from facturacion_electronica.helpers import preparar_facturas
from util.helpers import generarDocumento, importarDocumento
from util.resources import ConsumoResource, ControlResource, MovimientoResource, SubsidioResource, ClienteResource

_DRIVE_SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# Per-worker cache: credentials and service are built once and reused across threads.
_state_lock = threading.Lock()
_creds = None
_service = None

def _refresh_state():
    """Load/refresh credentials and rebuild service if needed. Must hold _state_lock."""
    global _creds, _service
    token_file = settings.GOOGLE_TOKEN_FILE
    if _creds is None:
        if not os.path.exists(token_file):
            token_json = os.environ.get('GOOGLE_TOKEN_JSON')
            if not token_json:
                raise RuntimeError('Google Drive no autorizado. Visita /google-auth/ para autorizar.')
            with open(token_file, 'w') as f:
                f.write(token_json)
        _creds = Credentials.from_authorized_user_file(token_file, _DRIVE_SCOPES)
    if _creds.expired and _creds.refresh_token:
        _creds.refresh(Request())
        try:
            with open(token_file, 'w') as f:
                f.write(_creds.to_json())
        except OSError:
            pass
    if not _creds.valid:
        raise RuntimeError('Google Drive no autorizado. Visita /google-auth/ para autorizar.')
    if _service is None:
        _service = build('drive', 'v3', credentials=_creds)

def _drive_creds():
    with _state_lock:
        _refresh_state()
        return _creds

def _drive_service():
    with _state_lock:
        _refresh_state()
        return _service

def _reset_drive_state():
    global _creds, _service
    with _state_lock:
        _creds = None
        _service = None

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
    state = request.GET.get('state')
    client_config = {
        'web': {
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_CLIENT_SECRET,
            'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
            'token_uri': 'https://oauth2.googleapis.com/token',
            'redirect_uris': [settings.GOOGLE_REDIRECT_URI],
        }
    }
    flow = Flow.from_client_config(client_config, scopes=_DRIVE_SCOPES,
                                   redirect_uri=settings.GOOGLE_REDIRECT_URI,
                                   state=state)
    os.environ.setdefault('OAUTHLIB_INSECURE_TRANSPORT', '1')
    flow.fetch_token(authorization_response=request.build_absolute_uri())
    creds = flow.credentials
    with open(settings.GOOGLE_TOKEN_FILE, 'w') as f:
        f.write(creds.to_json())
    _reset_drive_state()
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
        creds = _drive_creds()
        session = AuthorizedSession(creds)
        url = f'https://www.googleapis.com/drive/v3/files/{file_id}?alt=media&supportsAllDrives=true'
        r = session.get(url, stream=True)
        r.raise_for_status()
        disposition = 'attachment' if request.GET.get('download') else 'inline'
        file_name = request.GET.get('nombre', 'factura.pdf')
        response = StreamingHttpResponse(r.iter_content(chunk_size=8192), content_type='application/pdf')
        response['Content-Disposition'] = f'{disposition}; filename="{file_name}"'
        response['X-Frame-Options'] = 'SAMEORIGIN'
        return response
    except Exception as e:
        return HttpResponse(f'Error al obtener el archivo: {e}', status=500)


def exportarConsumos(request):
    dataset = ConsumoResource().export()
