# -*- coding: utf-8 -*-
import yaml
from mock import patch
from mock_open import MockOpen

from sanitized_dump.config import Configuration
from sanitized_dump.utils import models
from sanitized_dump.utils.compat import builtins_open


def assert_all_models_in_conf(config):
    model_table_names = models.get_model_table_names()
    assert all(model_name in config['strategy'] for model_name in model_table_names)


def assert_config_sections(config):
    assert all(key in config for key in ['config', 'strategy'])


def assert_all_model_fields_in_conf(config):
    assert models.validate_all_model_fields_in_config(config)


class TestConfiguration(object):
    def test_create_from_models(self):
        configuration_instance = Configuration.from_models()
        config = configuration_instance.config

        assert_config_sections(config)
        assert_all_model_fields_in_conf(config)

    @patch(builtins_open, new_callable=MockOpen)
    def test_create_from_file(self, mocked_open):
        Configuration().write_configuration_file()
        with open(Configuration().standard_file_path, 'r') as conf_file:
            config = Configuration.from_file(conf_file)
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
            conf = yaml.load(conf_file)
            assert_all_model_fields_in_conf(conf)
