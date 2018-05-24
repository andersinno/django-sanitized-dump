# -*- coding: utf-8 -*-

import pytest

from sanitized_dump.utils import models


def test_get_models():
    result = models.get_models()
    names = sorted(_get_model_name(model) for model in result)
    assert names == [
        'admin:LogEntry',
        'auth:Group',
        'auth:Permission',
        'auth:User',
        'contenttypes:ContentType',
        'sessions:Session',
        'testapp:Name',
        'testapp:Secret',
    ]


EXPECTED_TABLES_AND_COLUMNS_BY_MODEL = {
    'auth:Group': {
        'auth_group': [
            'id',
            'name',
        ],
        'auth_group_permissions': [
            'id',
            'group_id',
            'permission_id',
        ],
    },
    'auth:User': {
        'auth_user': [
            'id',
            'password',
            'last_login',
            'is_superuser',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_staff',
            'is_active',
            'date_joined',
        ],
        'auth_user_groups': [
            'id',
            'user_id',
            'group_id',
        ],
        'auth_user_user_permissions': [
            'id',
            'user_id',
            'permission_id',
        ],
    },
    'testapp:Name': {
        'testapp_name': [
            'id',
            'name',
        ],
    },
    'testapp:Secret': {
        'testapp_secret': [
            'id',
            'name',
            'text',
        ],
    },
}


@pytest.mark.parametrize(
    'model_name', EXPECTED_TABLES_AND_COLUMNS_BY_MODEL.keys())
def test_get_db_tables_and_columns_of_model(model_name):
    expected = EXPECTED_TABLES_AND_COLUMNS_BY_MODEL[model_name]
    for model in models.get_models():
        if _get_model_name(model) == model_name:
            result = models.get_db_tables_and_columns_of_model(model)
            assert result == expected


def test_get_model_table_to_model_map():
    assert models.get_model_table_to_model_name_map() == {
        'auth_group': 'Group',
        'auth_group_permissions': 'Group_permissions',
        'auth_permission': 'Permission',
        'auth_user': 'User',
        'auth_user_groups': 'User_groups',
        'auth_user_user_permissions': 'User_user_permissions',
        'django_admin_log': 'LogEntry',
        'django_content_type': 'ContentType',
        'django_session': 'Session',
        'testapp_name': 'Name',
        'testapp_secret': 'Secret',
    }


def _get_model_name(model):
    return '{}:{}'.format(model._meta.app_label, model.__name__)
