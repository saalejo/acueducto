from django.contrib import admin
from .models import Consumo, Control, Elemento, Movimiento, Subsidio

admin.site.site_header = 'Acueducto'
admin.site.register(Control)
admin.site.register(Consumo)
admin.site.register(Movimiento)
admin.site.register(Subsidio)
admin.site.register(Elemento)
