from itertools import chain

import django

try:
    from django.apps import apps
    get_models = apps.get_models
except ImportError:
    # Django < 1.7
    from django.db.models import get_models


def get_model_table_name(model):
    return model._meta.db_table


def get_model_field_names(model):
    """
    Get all fields of a models

    In Django 1.10 the function get_all_field_names() was
    removed and can no longer be used. The Django documentation [1]
    suggests two replacement options of which this is the
    100% backwards compatible version. A simpler solution would be
    `[f.name for f in model._meta.get_fields()]`. But we try to keep
    backward compatibility as well as possible for now.

    [1] https://docs.djangoproject.com/en/1.9/ref/models/meta/#migrating-from-the-old-api
    """
    if django.VERSION < (1, 8, 0):
        return model._meta.get_all_field_names()

    return list(set(chain.from_iterable(
        (field.name, field.attname) if hasattr(field, 'attname') else (field.name,)
        for field in model._meta.get_fields()
        # For complete backwards compatibility, you may want to exclude
        # GenericForeignKey from the results.
        if not (field.many_to_one and field.related_model is None)
    )))


def get_model_table_names():
    models = get_models()
    return [get_model_table_name(model) for model in models]


def get_model_table_map():
    models = get_models()
    return {get_model_table_name(model): model for model in models}


def get_model_table_to_model_name_map():
    models = get_models()
    return {get_model_table_name(model): model.__name__ for model in models}
