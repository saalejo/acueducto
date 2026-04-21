from django.core.management.base import BaseCommand, CommandError
from facturacion_electronica.helpers import preparar_facturas
from util.models import *

class Command(BaseCommand):
    help = 'Preparar_facturas'

    def handle(self, *args, **options):
        preparar_facturas()