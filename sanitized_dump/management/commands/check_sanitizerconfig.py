from sanitized_dump.config import Configuration
from sanitized_dump.management.base_commands import DBReadonlyCommand
from sanitized_dump.utils.models import get_model_table_to_model_name_map


class Command(DBReadonlyCommand):
    help = 'Check .sanitizerconfig is up to date with models'

    def handle(self, *args, **options):
        self.stdout.write('Comparing models and sanitizer config...')
        conf = Configuration.from_standard_config_file()
        table_to_model_map = get_model_table_to_model_name_map()
        diff = conf.diff_with_models

        if not diff:
            self.stdout.write('IN SYNC: {} is up to date with your models.'.format(
                Configuration.standard_file_name
            ))
            return

        for table_name, fields in diff.items():
            for field in fields:
                self.stdout.write('Missing field from {conf_file}: {model}.{field}'.format(**{
                    'model': table_to_model_map[table_name],
                    'field': field,
                    'conf_file': Configuration.standard_file_name,
                }))

        raise SystemExit('OUT OF SYNC: {} is not up to date with your models.'.format(
            Configuration.standard_file_name
        ))
