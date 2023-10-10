from datetime import datetime
from import_export import resources
from import_export.fields import Field
from import_export.widgets import NumberWidget
from .models import Consumo, Control, Movimiento, Subsidio, Cliente

class MyFloat(NumberWidget):
    def clean(self, value, row=None, **kwargs):
        if self.is_empty(value):
            return None
        return float("{:.2f}".format(value))

class ControlResource(resources.ModelResource):
    class Meta:
        model = Control

class ConsumoResource(resources.ModelResource):
    codacu = Field(attribute='codacu')
    vereda = Field(attribute='vereda')
    sector = Field(attribute='sector')
    ruta = Field(attribute='ruta', widget=MyFloat())
    codcte = Field(attribute='codcte')
    lecact = Field(attribute='lecact', widget=MyFloat())
    feccon = Field(attribute='feccon')
    lecant = Field(attribute='lecant', widget=MyFloat())
    consumo = Field(attribute='consumo', widget=MyFloat())
    indliq = Field(attribute='indliq')
    enero = Field(attribute='enero', widget=MyFloat())
    conenero = Field(attribute='conenero', widget=MyFloat())
    febrero = Field(attribute='febrero', widget=MyFloat())
    confebrero = Field(attribute='confebrero', widget=MyFloat())
    marzo = Field(attribute='marzo', widget=MyFloat())
    conmarzo = Field(attribute='conmarzo', widget=MyFloat())
    abril = Field(attribute='abril', widget=MyFloat())
    conabril = Field(attribute='conabril', widget=MyFloat())
    mayo = Field(attribute='mayo', widget=MyFloat())
    conmayo = Field(attribute='conmayo', widget=MyFloat())
    junio = Field(attribute='junio', widget=MyFloat())
    conjunio = Field(attribute='conjunio', widget=MyFloat())
    julio = Field(attribute='julio', widget=MyFloat())
    conjulio = Field(attribute='conjulio', widget=MyFloat())
    agosto = Field(attribute='agosto', widget=MyFloat())
    conagosto = Field(attribute='conagosto', widget=MyFloat())
    septiembre = Field(attribute='septiembre', widget=MyFloat())
    conseptiem = Field(attribute='conseptiem', widget=MyFloat())
    octubre = Field(attribute='octubre', widget=MyFloat())
    conoctubre = Field(attribute='conoctubre', widget=MyFloat())
    noviembre = Field(attribute='noviembre', widget=MyFloat())
    connoviemb = Field(attribute='connoviemb', widget=MyFloat())
    diciembre = Field(attribute='diciembre', widget=MyFloat())
    condiciemb = Field(attribute='condiciemb', widget=MyFloat())
    
    class Meta:
        model = Consumo
        import_id_fields = ['codcte']
        exclude = ['id', 'ultimoMes',]

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