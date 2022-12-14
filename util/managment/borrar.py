from django.core.management.base import BaseCommand, CommandError
from util.models import *

class Command(BaseCommand):
    help = 'Borrar todo'

    def handle(self, *args, **options):
        Control.objects.all().delete()
        Consumo.objects.all().delete()
        Movimiento.objects.all().delete()
        Subsidio.objects.all().delete()