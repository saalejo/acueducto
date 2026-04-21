from django.db import models

class Resolucion(models.Model):
    prefijo = models.CharField(max_length=10)
    numero = models.IntegerField(default=0)
    llave_tecnica = models.CharField(max_length=64)
    desde = models.IntegerField(default=0)
    hasta = models.IntegerField(default=0)
    consecutivo = models.IntegerField(default=0)
    fecha_desde = models.DateField(auto_now=True)
    fecha_hasta = models.DateField(auto_now=True)
    activa = models.BooleanField(default=True)
    
    def __str__(self):
        return str(self.numero)
    
    class Meta:
        verbose_name_plural = "resoluciones"


class Apidian(models.Model):
    url = models.CharField(max_length=64)
    nit = models.CharField(max_length=16, default="")
    token_api = models.CharField(max_length=64)
    token_dian = models.CharField(max_length=64, default="")
    certificate = models.TextField(default="")
    password = models.CharField(max_length=16, default="")
    software_id = models.CharField(max_length=64, default="")
    pin = models.CharField(max_length=16, default="")
    technical_key = models.CharField(max_length=64, default="")
    ambiente = models.CharField(max_length=16, default="")
    
    def __str__(self):
        return self.url

class Entidad(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100,null=True)
    celular = models.CharField(max_length=100,null=True)
    email = models.CharField(max_length=100,null=True)
    direccion = models.CharField(max_length=100,null=True)
    registroMercantil = models.CharField(max_length=100,null=True, default='0000-00')
    TIPO_CHOICES = (
        (1, 'Registro civil'),
        (2, 'Tarjeta de identidad'),
        (3, 'Cédula de ciudadanía'),
        (4, 'Tarjeta de extranjería'),
        (5, 'Cédula de extranjería'),
        (6, 'NIT'),
        (7, 'Pasaporte'),
        (8, 'Documento de identificación extranjero'),
        (9, 'NIT de otro país'),
        (10, 'NUIP *'),
    )
    tipoIdentificacion = models.IntegerField(choices=TIPO_CHOICES,default=3,null=True)
    TIPO_ORGANIZACION_CHOICES = (
        (1, 'Persona Jurídica'),
        (2, 'Persona Natural'),
    )
    tipoOrganizacion = models.IntegerField(choices=TIPO_ORGANIZACION_CHOICES,default=2,null=True)
    REGIMEN_CHOICES = (
        (1, 'Responsable de iva'),
        (2, 'No responsable de iva'),
    )
    regimen = models.IntegerField(choices=REGIMEN_CHOICES,default=2,null=True)
    identificacion = models.CharField(max_length=100,null=True,)
    CIUDAD_CHOICES = (
        (33, 'El Carmen de Viboral'),
        (1, 'Medellin'),
    )
    ciudad = models.IntegerField(choices=CIUDAD_CHOICES,default=33,null=True)
    fecha = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
    
    def tipo_documento_name(self):
        for choice in self.TIPO_CHOICES:
            if choice[0] == self.tipoIdentificacion:
                return choice[1]
        return ''

    class Meta:
        verbose_name_plural = "entidades"
        ordering = ["pk"]

class Filaimpuesto(models.Model):
    cod = models.IntegerField(default=0)
    cargo = models.BooleanField(default=False)
    concepto = models.CharField(max_length=100)
    cantidad = models.IntegerField(default=0)
    cantidad_base = models.IntegerField(default=0)
    porcentaje = models.IntegerField(default=0)

class Filadescuento(models.Model):
    cod = models.IntegerField(default=0)
    cargo = models.BooleanField(default=False)
    concepto = models.CharField(max_length=100)
    cantidad = models.IntegerField(default=0)
    cantidad_base = models.IntegerField(default=0)
    
class Factura(models.Model):
    consecutivo = models.IntegerField()
    contabilizada = models.BooleanField(default=False)
    es_valida = models.BooleanField(default=False)
    ESTADO_CHOICES = (        
        ('aprobado', 'Aprobado'),
        ('anulado', 'Anulado'),
    )
    estado = models.CharField(choices=ESTADO_CHOICES,max_length=8, default='aprobado')
    referencia = models.IntegerField(default=0)
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)
    FORMA_PAGO_CHOICES = (        
        (1, 'Contado'),
        (2, 'Crédito'),
    )
    formaPago = models.IntegerField(choices=FORMA_PAGO_CHOICES, default=1)
    METODO_PAGO_CHOICES = (        
        (10, 'Efectivo'),
        (20, 'Cheque'),    
        (30, 'Transferecia Crédito'),
        (32, 'Transferencia Débito'),        
    )
    metodoPago = models.IntegerField(choices=METODO_PAGO_CHOICES, default=10)
    ESTADO_CUENTA_CHOICES = (        
        ('pagada', 'Pagada'),
        ('pendiente', 'Pendiente'),
        ('mora', 'Mora'),
    )
    estadoCuenta = models.CharField(max_length=10,choices=ESTADO_CUENTA_CHOICES,default='pagada')
    fecha = models.DateField(auto_now=True)
    hora = models.TimeField(auto_now=True)
    fechaPago = models.DateTimeField(auto_now=True)
    prefactura = models.IntegerField(default=0)
    plazo = models.IntegerField(default=0)
    importe = models.IntegerField(default=0)
    total = models.IntegerField(default=0)    
    totalPagar = models.IntegerField(default=0)   
    sumImpuestos = models.IntegerField(default=0)
    sumDescuentos = models.IntegerField(default=0, null=True)
    pendiente = models.IntegerField(default=0)
    totalPagado = models.IntegerField(default=0)
    cambio = models.IntegerField(default=0)
    fe_json = models.JSONField(null=True,blank=True, default=None)
    resp_dian = models.JSONField(null=True,blank=True, default=None)
    cufe = models.CharField(max_length=128, null=True,blank=True, default=None)
    zip_code = models.CharField(max_length=128, null=True,blank=True, default=None)
        
    def __str__(self):
        return str(self.pk)
    
    class Meta:
        ordering = ['-pk']

class Notadebito(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    consecutivo = models.IntegerField()
    es_credito = models.BooleanField(default=False)
    json = models.JSONField(null=True,blank=True, default=None)
    resp_dian = models.JSONField(null=True,blank=True, default=None)
    cude = models.CharField(max_length=128, null=True,blank=True, default=None)
    zip_code = models.CharField(max_length=128, null=True,blank=True, default=None)

class Notacredito(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    consecutivo = models.IntegerField()
    es_credito = models.BooleanField(default=False)
    json = models.JSONField(null=True,blank=True, default=None)
    resp_dian = models.JSONField(null=True,blank=True, default=None)
    cude = models.CharField(max_length=128, null=True,blank=True, default=None)
    zip_code = models.CharField(max_length=128, null=True,blank=True, default=None)
    
class Facturaimpuesto(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    cod = models.IntegerField(default=0)
    cargo = models.BooleanField(default=False)
    concepto = models.CharField(max_length=100)
    cantidad = models.IntegerField(default=0)
    cantidad_base = models.IntegerField(default=0)
    porcentaje = models.IntegerField(default=0)

class Facturadescuento(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    cod = models.IntegerField(default=0)
    cargo = models.BooleanField(default=False)
    concepto = models.CharField(max_length=100)
    cantidad = models.IntegerField(default=0)
    cantidad_base = models.IntegerField(default=0)

class Fila(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    descripcion = models.TextField(default=None,null=True,blank=True)
    cedula = models.CharField(max_length=15,default='',null=True,blank=True)
    cantidad = models.IntegerField(default=0)
    unidad_de_medida_cod = models.CharField(max_length=256, null=True, default=None, blank=True)
    unidad_de_medida_name = models.CharField(max_length=256, null=True, default=None, blank=True)
    talla = models.CharField(max_length=50, null=True, default=None, blank=True)
    valorUnitario = models.IntegerField(default=0)
    descuento = models.IntegerField(default=0)
    importe = models.IntegerField(default=0)
    fecha = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.pk)
