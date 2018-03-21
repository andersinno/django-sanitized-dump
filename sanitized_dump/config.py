import yaml

from .utils.models import (
    get_model_table_name,
    get_model_field_names,
    get_models
)

class Configuration:
    def __init__(self, config=None):
        self.config = config if config else Configuration._get_initial_structure()

    @classmethod
    def from_models(cls):
        configuration = Configuration()
        models = get_models()

        for model in models:
            configuration.add_empty_model_strategy(model)

        return configuration

    def _get_initial_structure():
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

    def write_configuration_file(self, file_path):
        with open(file_path, "w") as config_file:
            yaml.dump(self.config, config_file, default_flow_style=False)
