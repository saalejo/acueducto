from django.core.management.base import BaseCommand, CommandError
from facturacion_electronica.helpers import consultar

class Command(BaseCommand):
    help = 'Consultar'
    
    def add_arguments(self, parser):
        parser.add_argument("factura_id", type=int)

    def handle(self, *args, **options):
        consultar(options["factura_id"])