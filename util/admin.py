from django.contrib import admin
from .models import *

admin.site.site_header = 'Acueducto'
admin.site.register(Control)
admin.site.register(Consumo)
admin.site.register(Cliente)
admin.site.register(Dispositivo)
admin.site.register(Elemento)
admin.site.register(Lectura)
admin.site.register(Movimiento)
admin.site.register(Ruta)
admin.site.register(Subsidio)
