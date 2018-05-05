from sanitized_dump.management.base_commands import DBReadonlyCommand
from subprocess import call
from django.conf import settings

from sanitized_dump.utils.db import db_setting_to_db_string


class Command(DBReadonlyCommand):
    help = 'Create sanitized database dump'

    def handle(self, *args, **options):
        self.stdout.write('Creating sanitized dump...')

        database_string = db_setting_to_db_string(settings.DATABASES)
        call(["database-sanitizer", '-c', '.sanitizerconfig', database_string])
