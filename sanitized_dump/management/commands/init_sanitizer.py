from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create a sanitizer configuration'

    def handle(self, *args, **options):
        self.stdout.write('Creating initial configuration...')
