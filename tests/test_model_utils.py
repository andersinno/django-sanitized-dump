# -*- coding: utf-8 -*-

from testapp.models import Name

from sanitized_dump.utils import models


class TestModelUtils():
    def test_get_model_table_name(self):
        assert models.get_model_table_name(Name) == 'testapp_name'
        assert True

    def test_get_model_table_names(self):
        model_table_names = [
            'auth_permission',
            'auth_group',
            'auth_user',
            'django_content_type',
            'django_admin_log',
            'django_session',
            'testapp_secret',
            'testapp_name'
        ]

        assert all(table_name in models.get_model_table_names() for table_name in model_table_names)

    def test_get_model_field_names(self):
        assert set(models.get_model_field_names(Name)) == set(['id', 'name'])

    def test_config_validation_empty_config(self):
        assert models.validate_all_model_fields_in_config({}) is False

    def test_config_validation_missing_models(self):
        config = {
            'strategy': {
                'bad_mode_name': {},
            }
        }
        assert models.validate_all_model_fields_in_config(config) is False

    def test_config_validation_missing_fields(self):
        config = {
            'strategy': {
                'testapp_secret': {},
            }
        }
        assert models.validate_all_model_fields_in_config(config) is False
