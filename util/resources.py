from import_export import resources
from .models import Consumo, Control, Movimiento, Subsidio

class ControlResource(resources.ModelResource):
    class Meta:
        model = Control

class ConsumoResource(resources.ModelResource):
    class Meta:
        model = Consumo

class MovimientoResource(resources.ModelResource):
    class Meta:
        model = Movimiento

class SubsidioResource(resources.ModelResource):
    class Meta:
        model = Subsidio