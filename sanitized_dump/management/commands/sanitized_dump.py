from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create sanitized database dump'

    def handle(self, *args, **options):
        self.stdout.write('Creating sanitized dump...')
