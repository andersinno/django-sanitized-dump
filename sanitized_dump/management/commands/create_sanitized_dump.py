from sanitized_dump.management.base_commands import DBReadonlyCommand
from subprocess import call
from django.conf import settings

from sanitized_dump.utils.db import db_setting_to_db_string


class Command(DBReadonlyCommand):
    help = 'Create sanitized database dump'

    def handle(self, verbosity=1, *args, **options):
        if verbosity >= 1:
            self.stderr.write('Creating sanitized dump...')

        database_string = db_setting_to_db_string(settings.DATABASES)
        call(["database-sanitizer", '-c', '.sanitizerconfig', database_string])
