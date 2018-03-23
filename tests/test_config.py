# -*- coding: utf-8 -*-
import pytest
import yaml
from mock import patch
from mock_open import MockOpen

from sanitized_dump.config import Configuration
from sanitized_dump.utils import models
from sanitized_dump.utils.compat import builtins_open
from testapp.models import Name, Secret


def assert_config_sections(config):
    assert all(key in config for key in ['config', 'strategy'])


class TestConfiguration(object):
    def test_create_from_models(self):
        configuration_instance = Configuration.from_models()
        config = configuration_instance.config

        assert_config_sections(config)
        assert configuration_instance.in_sync_with_models

    @patch(builtins_open, new_callable=MockOpen)
    def test_create_from_file(self, mocked_open):
        Configuration().write_configuration_file()
        with open(Configuration().standard_file_path, 'r') as conf_file:
            config = Configuration.from_file(conf_file)
            assert config.config

    @patch(builtins_open, new_callable=MockOpen)
    def test_create_from_file_path(self, mocked_open):
        Configuration().write_configuration_file()
        with open(Configuration().standard_file_path, 'r') as conf_file:
            config = Configuration.from_file_path(conf_file.name)
            assert config.config

    @patch(builtins_open, new_callable=MockOpen)
    def test_write_empty_configuration_file(self, mocked_open):
        Configuration().write_configuration_file()
        with open(Configuration().standard_file_path, 'r') as conf_file:
            conf = yaml.load(conf_file)
            assert conf

    @patch(builtins_open, new_callable=MockOpen)
    def test_write_full_configuration_file(self, mocked_open):
        config = Configuration.from_models()
        config.write_configuration_file()
        with open(Configuration().standard_file_path, 'r') as conf_file:
            conf = Configuration(yaml.load(conf_file))
            assert conf.in_sync_with_models

    def test_empty_config_is_not_valid(self):
        Configuration({}).validate()

    @patch('sanitized_dump.config.get_models', return_value=[Name])
    def test_diff_with_missing_model(self, mocked_get_models):
        config = Configuration({
            'config': {},
            'strategy': {}
        })
        assert config.diff_with_models == {
            'testapp_name': set(['id', 'name'])
        }

    @patch('sanitized_dump.config.get_models', return_value=[Secret])
    def test_diff_with_missing_fields(self, mocked_get_models):
        config = Configuration({
            'config': {},
            'strategy': {
                'testapp_secret': {},
            }
        })
        assert config.diff_with_models == {
            'testapp_secret': set(['id', 'name', 'text'])
        }
