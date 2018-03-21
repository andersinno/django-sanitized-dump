import os

from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from sanitized_dump.config import Configuration


class Command(BaseCommand):
    help = 'Create a sanitizer configuration'

    def handle(self, *args, **options):
        self.stdout.write('Creating initial configuration...')
        conf = Configuration.from_models()
        filepath = conf.standard_file_path
        try:
            conf.write_configuration_file()
            self.stdout.write('Created {}'.format(filepath))
        except OSError:
            self.stderr.write('Failed creating {}'.format(filepath))

