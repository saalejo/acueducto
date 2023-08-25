from util.helpers import crearRuta
from .models import Ruta, Dispositivo
from django.db.models.signals import post_save
from django.dispatch import receiver
import secrets


@receiver(post_save, sender=Dispositivo)
def after_save_dispositivo(sender, instance, created, **kwargs):
    if created:
        token = secrets.token_hex(nbytes=16)
        Dispositivo.objects.filter(pk=instance.pk).update(codigo=token)

@receiver(post_save, sender=Ruta)
def after_save_ruta(sender, instance, created, **kwargs):
    if created:
        crearRuta(instance)