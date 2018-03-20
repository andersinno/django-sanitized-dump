# -*- coding: utf-8 -*-
from django.test import TestCase

from testapp.models import Name
from sanitized_dump.utils import models


class TestModelUtils():
    def test_get_model_table_name(self):
        print(models.get_model_table_name(Name))
        assert models.get_model_table_name(Name) == 'testapp_name'
        assert True

    def test_get_model_field_names(self):
        print(models.get_model_field_names(Name))
        assert models.get_model_field_names(Name) == ['id', 'name']