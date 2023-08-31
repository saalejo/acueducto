from import_export import resources
from .models import Consumo, Control, Movimiento, Subsidio, Cliente

class ControlResource(resources.ModelResource):
    class Meta:
        model = Control

class ConsumoResource(resources.ModelResource):
    class Meta:
        model = Consumo
        import_id_fields = ['codcte']
        fields = [
            'codacu', 'vereda', 'sector', 'ruta', 'codcte',
            'lecact', 'feccon', 'lecant', 'consumo', 'indliq',
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