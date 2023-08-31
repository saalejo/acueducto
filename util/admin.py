from django.contrib import admin

from util.resources import *
from .models import *
from import_export.admin import ImportExportModelAdmin

class ConsumoAdmin(ImportExportModelAdmin):
    resource_classes = [ConsumoResource]
    list_per_page = 1000

class ClienteAdmin(ImportExportModelAdmin):
    resource_classes = [ClienteResource]
    list_per_page = 1000

admin.site.site_header = 'Acueducto'
admin.site.register(Control)
admin.site.register(Consumo, ConsumoAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Dispositivo)
admin.site.register(Elemento)
admin.site.register(Lectura)
admin.site.register(Movimiento)
admin.site.register(Ruta)
admin.site.register(Subsidio)
