import pytest
from django.core.management import call_command
from mock import patch
from mock_open import MockOpen
from six import StringIO

from sanitized_dump.config import Configuration
from sanitized_dump.utils.compat import builtins_open


@patch(builtins_open, new_callable=MockOpen)
def test_init_sanitizer(mocked_open):
    output = StringIO()
    call_command('init_sanitizer', stdout=output)
    with open(Configuration.standard_file_path) as conf_file:
        conf = Configuration.from_file(conf_file)
        assert conf.in_sync_with_models


@patch(builtins_open, new_callable=MockOpen)
def test_check_sanitizerconfig(mocked_open):
    """
    Run check_sanitizerconfig in the testapp and expect it
    to return False since the project is missing configuration.
    """
    output = StringIO()
    err = StringIO()
    with pytest.raises(SystemExit) as e:
        call_command('check_sanitizerconfig', stderr=err, stdout=output)
        assert 'OUT OF SYNC' in str(e)
    assert 'IN SYNC' not in output.getvalue()

    output = StringIO()
    err = StringIO()
    call_command('init_sanitizer', stderr=err, stdout=output)
    call_command('check_sanitizerconfig', stderr=err, stdout=output)
    assert 'OUT OF SYNC' not in err.getvalue()
    assert 'IN SYNC' in output.getvalue()
