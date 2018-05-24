try:
    from django.apps import apps
    get_models = apps.get_models
except ImportError:
    # Django < 1.7
    from django.db.models import get_models


def get_db_tables_and_columns_of_model(model):
    all_models = [model] + _get_m2m_through_models_of_model(model)
    return {
        _get_table_name(item): _get_columns(item._meta.local_fields)
        for item in all_models
    }


def _get_m2m_through_models_of_model(model):
    return [
        _get_remote_field(field).through
        for field in model._meta.local_many_to_many
        if _get_remote_field(field).through._meta.auto_created
    ]


def _get_remote_field(field):
    if hasattr(field, 'remote_field'):  # Django >= 1.9
        return field.remote_field
    return field.rel  # Django <= 1.8


def _get_table_name(model):
    return model._meta.db_table


def _get_columns(fields):
    return [field.column for field in fields if field.column]


def get_model_table_to_model_name_map():
    models = get_models()
    result = {}
    for original_model in models:
        m2m_models = _get_m2m_through_models_of_model(original_model)
        for model in [original_model] + m2m_models:
            result[_get_table_name(model)] = model.__name__
    return result
