from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create sanitized database dump'

    def handle(self, *args, **options):
        # TODO: Create a database dump using the current django settings and then sanitize the data
        # and warn about diffs between the current model state and the sanitizer configuration.
        self.stdout.write('Creating sanitized dump...')
