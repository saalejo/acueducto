import datetime
from util.helpers import crearRuta
from .models import Consumo, Ruta, Dispositivo
from django.db.models.signals import post_save
from django.dispatch import receiver
import secrets
import xlrd


@receiver(post_save, sender=Dispositivo)
def after_save_dispositivo(sender, instance, created, **kwargs):
    if created:
        token = secrets.token_hex(nbytes=16)
        Dispositivo.objects.filter(pk=instance.pk).update(codigo=token)

@receiver(post_save, sender=Ruta)
def after_save_ruta(sender, instance, created, **kwargs):
    if created:
        crearRuta(instance)

@receiver(post_save, sender=Consumo)
def after_save_consumo(sender, instance, **kwargs):
    if isinstance(instance.feccon, float):
        date = xlrd.xldate_as_datetime(instance.feccon, 0)
        Consumo.objects.filter(pk=instance.pk).update(feccon=date.date())
