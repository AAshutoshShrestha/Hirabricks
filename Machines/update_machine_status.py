# update_machine_status.py

from django.core.management.base import BaseCommand
from .views import machine_status_update

class Command(BaseCommand):
    help = 'Update machine status'

    def handle(self, *args, **options):
        machine_status_update()
