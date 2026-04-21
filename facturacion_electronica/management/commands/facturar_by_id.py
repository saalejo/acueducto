from django.core.management.base import BaseCommand, CommandError
from facturacion_electronica.helpers import facturar
from util.models import *

class Command(BaseCommand):
    help = 'Facturar'
    
    def add_arguments(self, parser):
        parser.add_argument("factura_id", type=int)

    def handle(self, *args, **options):
        facturar(options["factura_id"])