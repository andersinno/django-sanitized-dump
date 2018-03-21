# -*- coding: utf-8 -*-

from sanitized_dump.utils import models
from testapp.models import Name


class TestModelUtils():
    def test_get_model_table_name(self):
        assert models.get_model_table_name(Name) == 'testapp_name'
        assert True

    def test_get_model_field_names(self):
        assert set(models.get_model_field_names(Name)) == set(['id', 'name'])
