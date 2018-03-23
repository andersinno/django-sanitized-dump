import os
from collections import defaultdict

import yaml
from django.conf import settings

from .utils.models import (
    get_model_field_names,
    get_model_table_name,
    get_models,
)

# TODO: Figure out a way to get the dir where manage.py is without BASE_DIR
BASE_DIR = getattr(settings, 'BASE_DIR', None)
assert BASE_DIR, 'Missing BASE_DIR in settings. Add it and retry.'


class Configuration(object):
    standard_file_name = '.sanitizerconfig'
    standard_file_path = os.path.join(BASE_DIR, standard_file_name)

    def __init__(self, config=None):
        self.config = config if config else Configuration._get_initial_structure()

    def __str__(self):
        return 'Configuration'

    @classmethod
    def from_models(cls):
        configuration = Configuration()
        models = get_models()

        for model in models:
            configuration.add_empty_model_strategy(model)

        return configuration

    @classmethod
    def from_file(cls, file):
        conf = Configuration(yaml.load(file))
        conf.validate()
        return conf

    @classmethod
    def from_file_path(cls, file_path):
        with open(file_path, "r") as config_file:
            return cls.from_file(config_file)

    @classmethod
    def from_standard_config_file(cls):
        return cls.from_file_path(cls.standard_file_path)

    @property
    def in_sync_with_models(self):
        return not bool(self.diff_with_models)

    @property
    def strategy(self):
        return self.config.get('strategy', {})

    @property
    def diff_with_models(self):
        """
        Return a dict stating the differences between current state of models
        and the configuration itself.
        TODO: Detect fields that are in conf, but not in models
        """
        missing_from_conf = defaultdict(set)

        for model in get_models():
            table_name = get_model_table_name(model)
            model_strategy = self.strategy.get(table_name)
            for model_field in get_model_field_names(model):
                if not model_strategy or model_field not in model_strategy.keys():
                    missing_from_conf[table_name].add(model_field)
        return missing_from_conf

    @strategy.setter
    def strategy(self, value):
        if not isinstance(value, (dict)):
            raise ValueError(
                'Invalid strategy: {} provided, should be dict.'.format(type(value))
            )
        return self.config.set('strategy', value)

    def validate(self):
        assert all(key in self.config for key in ['config', 'strategy'])
        assert isinstance(self.config['config'], dict)
        assert isinstance(self.config['strategy'], dict)
        assert isinstance(self.config['config'].get('addons'), list)

    @classmethod
    def _get_initial_structure(cls):
        return {
            "config": {
                "addons": [],
            },
            "strategy": {},
        }

    def add_empty_model_strategy(self, model):
        model_table_name = get_model_table_name(model)
        model_field_names = get_model_field_names(model)

        field_name_strategy = {
            field_name: None for field_name in model_field_names
        }

        self.config['strategy'][model_table_name] = field_name_strategy

    def write_configuration_file(self, file_path=standard_file_path):
        with open(file_path, "w") as config_file:
            yaml.dump(self.config, config_file, default_flow_style=False)
