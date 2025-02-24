import os
import json
import yaml
import copy
from jsonschema import validate as jsonschema_validate, ValidationError

from config_manager.exceptions import ConfigValidationError, ConfigLoaderError

def enforce_no_additional_properties(schema):
    """Recursively enforce that objects do not allow additional properties."""
    if isinstance(schema, dict):
        if schema.get("type") == "object":
            # Do not allow properties not explicitly defined
            schema.setdefault("additionalProperties", False)
            if "properties" in schema:
                for prop in schema["properties"].values():
                    enforce_no_additional_properties(prop)
        elif schema.get("type") == "array" and "items" in schema:
            enforce_no_additional_properties(schema["items"])
    return schema

class ConfigManager:
    def __init__(self):
        self.config = {}

    def load_configs(self, configs):
        for conf in configs:
            if isinstance(conf, dict):
                self._merge_config(conf)
            elif isinstance(conf, str):
                if conf.startswith("env://"):
                    prefix = conf[len("env://"):]
                    env_config = {}
                    for key, value in os.environ.items():
                        if key.startswith(prefix):
                            new_key = key[len(prefix):].lower().replace('_', '.')
                            if value.isdigit():
                                converted = int(value)
                            else:
                                try:
                                    converted = float(value)
                                except ValueError:
                                    converted = value
                            self._set_key(env_config, new_key.split('.'), converted)
                    self._merge_config(env_config)
                else:
                    try:
                        if conf.endswith('.json'):
                            with open(conf, 'r') as f:
                                loaded = json.load(f)
                        elif conf.endswith(('.yaml', '.yml')):
                            with open(conf, 'r') as f:
                                loaded = yaml.safe_load(f)
                        else:
                            raise ConfigLoaderError("Unsupported file type: " + conf)
                        self._merge_config(loaded)
                    except Exception as e:
                        raise ConfigLoaderError(str(e))
        return self.config

    def _merge_config(self, new_config):
        self.config = self._deep_merge(self.config, new_config)

    def _deep_merge(self, base, new):
        for key, value in new.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                base[key] = self._deep_merge(base[key], value)
            else:
                base[key] = value
        return base

    def _set_key(self, d, keys, value):
        for key in keys[:-1]:
            d = d.setdefault(key, {})
        d[keys[-1]] = value

    def get(self, dotted_key):
        keys = dotted_key.split('.')
        d = self.config
        for key in keys:
            if not isinstance(d, dict) or key not in d:
                return None
            d = d[key]
        return d

    def validate(self, schema):
        # Create a copy of the schema and enforce no additional properties.
        schema_copy = copy.deepcopy(schema)
        enforce_no_additional_properties(schema_copy)
        try:
            jsonschema_validate(instance=self.config, schema=schema_copy)
        except ValidationError as e:
            path = ".".join([str(x) for x in e.path]) if e.path else "root"
            raise ConfigValidationError(f"Validation error in '{path}': {e.message}")