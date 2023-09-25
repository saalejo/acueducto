from datetime import datetime
from import_export import resources
from import_export.fields import Field
from import_export.widgets import DateWidget
from .models import Consumo, Control, Movimiento, Subsidio, Cliente

class ControlResource(resources.ModelResource):
    class Meta:
        model = Control

class ConsumoResource(resources.ModelResource):
    codacu = Field(attribute='codacu')
    vereda = Field(attribute='vereda')
    sector = Field(attribute='sector')
    ruta = Field(attribute='ruta')
    codcte = Field(attribute='codcte')
    lecact = Field(attribute='lecact')
    feccon = Field(attribute='feccon', widget=DateWidget(format='%d/%m/%Y'))
    
    class Meta:
        model = Consumo
        import_id_fields = ['codcte']
        fields = [
            'lecant', 'consumo', 'indliq',
            'enero', 'conenero',
            'febrero', 'confebrero',
            'marzo', 'conmarzo',
            'abril', 'conabril',
            'mayo', 'conmayo',
            'junio', 'conjunio',
            'julio', 'conjulio',
            'agosto', 'conagosto',
            'septiembre', 'conseptiem',
            'octubre', 'conoctubre',
            'noviembre', 'connoviemb',
            'diciembre', 'condiciemb'
        ]

class MovimientoResource(resources.ModelResource):
    class Meta:
        model = Movimiento

class SubsidioResource(resources.ModelResource):
    class Meta:
        model = Subsidio
class ClienteResource(resources.ModelResource):
    class Meta:
        model = Cliente
        import_id_fields = ['codcte']