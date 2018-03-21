# -*- coding: utf-8 -*-
from django.test import TestCase

from sanitized_dump.utils import models
from sanitized_dump.config import Configuration

from testapp.models import Secret

class TestModelUtils:
    def test_create_from_models(self):
        model_table_names = models.get_model_table_names()
        configuration_instance = Configuration.from_models()
        config = configuration_instance.config

        assert all(key in config for key in ['config', 'strategy'])
        assert all(model_name in config['strategy'] for model_name in model_table_names)
