from django.db import models

class Control(models.Model):
    empresa = models.CharField(max_length=255, null=True, blank=True, default=None)
    codemp = models.CharField(max_length=255, null=True, blank=True, default=None)
    nit = models.CharField(max_length=255, null=True, blank=True, default=None)
    codage = models.CharField(max_length=255, null=True, blank=True, default=None)
    nomage = models.CharField(max_length=255, null=True, blank=True, default=None)
    repleg = models.CharField(max_length=255, null=True, blank=True, default=None)
    ultcte = models.CharField(max_length=255, null=True, blank=True, default=None)
    fecpag = models.CharField(max_length=255, null=True, blank=True, default=None)
    desde = models.CharField(max_length=255, null=True, blank=True, default=None)
    hasta = models.CharField(max_length=255, null=True, blank=True, default=None)
    dias = models.CharField(max_length=255, null=True, blank=True, default=None)
    
    def __str__(self):
        return self.empresa
    
    class Meta:
        verbose_name_plural = "controles"
        # unique_together = ('empresa', 'codemp', 'nit')

class Consumo(models.Model):
    vereda = models.CharField(max_length=255, null=True, blank=True, default=None)
    codcte = models.CharField(max_length=255, null=True, blank=True, default=None)
    lecact = models.CharField(max_length=255, null=True, blank=True, default=None)
    feccon = models.CharField(max_length=255, null=True, blank=True, default=None)
    lecant = models.CharField(max_length=255, null=True, blank=True, default=None)
    indliq = models.CharField(max_length=255, null=True, blank=True, default=None)
    enero = models.CharField(max_length=255, null=True, blank=True, default=None)
    conenero = models.CharField(max_length=255, null=True, blank=True, default=None)
    febrero = models.CharField(max_length=255, null=True, blank=True, default=None)
    confebrero = models.CharField(max_length=255, null=True, blank=True, default=None)
    marzo = models.CharField(max_length=255, null=True, blank=True, default=None)
    conmarzo = models.CharField(max_length=255, null=True, blank=True, default=None)
    abril = models.CharField(max_length=255, null=True, blank=True, default=None)
    conabril = models.CharField(max_length=255, null=True, blank=True, default=None)
    mayo = models.CharField(max_length=255, null=True, blank=True, default=None)
    conmayo = models.CharField(max_length=255, null=True, blank=True, default=None)
    junio = models.CharField(max_length=255, null=True, blank=True, default=None)
    conjunio = models.CharField(max_length=255, null=True, blank=True, default=None)
    julio = models.CharField(max_length=255, null=True, blank=True, default=None)
    conjulio = models.CharField(max_length=255, null=True, blank=True, default=None)
    agosto = models.CharField(max_length=255, null=True, blank=True, default=None)
    conagosto = models.CharField(max_length=255, null=True, blank=True, default=None)
    septiembre = models.CharField(max_length=255, null=True, blank=True, default=None)
    conseptiembre = models.CharField(max_length=255, null=True, blank=True, default=None)
    octubre = models.CharField(max_length=255, null=True, blank=True, default=None)
    conoctubre = models.CharField(max_length=255, null=True, blank=True, default=None)
    noviembre = models.CharField(max_length=255, null=True, blank=True, default=None)
    connoviembre = models.CharField(max_length=255, null=True, blank=True, default=None)
    diciembre = models.CharField(max_length=255, null=True, blank=True, default=None)
    condiciembre = models.CharField(max_length=255, null=True, blank=True, default=None)
    
    def __str__(self):
        return self.codcte
    
    # class Meta:
    #     unique_together = ('codcte', 'feccon')

class Movimiento(models.Model):
    codage = models.CharField(max_length=255, null=True, blank=True, default=None)
    numdoc = models.CharField(max_length=255, null=True, blank=True, default=None)
    numcom = models.CharField(max_length=255, null=True, blank=True, default=None)
    codcon = models.CharField(max_length=255, null=True, blank=True, default=None)
    fecmvt = models.CharField(max_length=255, null=True, blank=True, default=None)
    codcta = models.CharField(max_length=255, null=True, blank=True, default=None)
    desmvt = models.CharField(max_length=255, null=True, blank=True, default=None)
    nitcte = models.CharField(max_length=255, null=True, blank=True, default=None)
    debito = models.CharField(max_length=255, null=True, blank=True, default=None)
    credito = models.CharField(max_length=255, null=True, blank=True, default=None)
    fecha = models.CharField(max_length=255, null=True, blank=True, default=None)
    
    def __str__(self):
        return self.nitcte
    
    class Meta:
    #     unique_together = ('nitcte', 'desmvt', 'fecha')
        ordering = ['nitcte', '-codcon']

class Subsidio(models.Model):
    factura = models.CharField(max_length=255, null=True, blank=True, default=None)
    fecmvt = models.CharField(max_length=255, null=True, blank=True, default=None)
    nitcte = models.CharField(max_length=255, null=True, blank=True, default=None)
    usuario = models.CharField(max_length=255, null=True, blank=True, default=None)
    cedula = models.CharField(max_length=255, null=True, blank=True, default=None)
    estrato = models.CharField(max_length=255, null=True, blank=True, default=None)
    debito = models.CharField(max_length=255, null=True, blank=True, default=None)
    abonosub = models.CharField(max_length=255, null=True, blank=True, default=None)
    saldosub = models.CharField(max_length=255, null=True, blank=True, default=None)
    vrpagado = models.CharField(max_length=255, null=True, blank=True, default=None)
    
    def __str__(self):
        return self.factura
    
    # class Meta:
    #     unique_together = ('factura', 'nitcte')

class Elemento(models.Model):
    nombre = models.CharField(max_length=255, null=True, blank=True, default=None)
    formula = models.CharField(max_length=255, null=True, blank=True, default=None)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ['nombre']
