from mock import patch
from mock_open import MockOpen

from django.core.management import call_command

from sanitized_dump.config import Configuration
from sanitized_dump.utils.compat import builtins_open


@patch(builtins_open, new_callable=MockOpen)
def test_init_sanitizer(mocked_open):
    call_command('init_sanitizer')
    with open(Configuration.standard_file_path) as conf_file:
        conf = Configuration.from_file(conf_file)
        assert conf.has_all_model_fields
