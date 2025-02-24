import pytest
import os
from config_manager import ConfigManager
from config_manager.exceptions import ConfigValidationError, ConfigLoaderError

class TestConfigManager:
    def test_basic_loading(self):
        config = ConfigManager()
        config.load_configs([{'database': {'host': 'localhost', 'port': 5432}}])
        
        assert config.get('database.host') == 'localhost'
        assert config.get('database.port') == 5432

    def test_priority_merging(self, tmp_path):
        config = ConfigManager()
        json_file = tmp_path / "test.json"
        json_file.write_text('{"database": {"host": "json_host", "port": 5432}}')
        
        config.load_configs([
            str(json_file),
            {'database': {'host': 'dict_host'}}
        ])
        
        assert config.get('database.host') == 'dict_host'
        assert config.get('database.port') == 5432

    def test_env_loading(self):
        config = ConfigManager()
        os.environ['APP_DB_HOST'] = 'env_host'
        os.environ['APP_DB_PORT'] = '5433'
        
        config.load_configs(['env://APP_'])
        
        assert config.get('db.host') == 'env_host'
        assert config.get('db.port') == 5433

    def test_validation(self):
        schema = {
            "type": "object",
            "properties": {
                "database": {
                    "type": "object",
                    "properties": {
                        "host": {"type": "string"},
                        "port": {"type": "number"}
                    },
                    "required": ["host"]
                }
            },
            "required": ["database"]
        }
        
        config = ConfigManager()
        config.load_configs([{'database': {'host': 'localhost'}}])
        config.validate(schema)
        
        with pytest.raises(ConfigValidationError):
            config.load_configs([{'invalid_key': 123}])
            config.validate(schema)
    
def test_validation_error_message():
    config = ConfigManager()
    config.load_configs([{"port": "invalid_number"}])
    
    schema = {
        "type": "object",
        "properties": {
            "port": {"type": "number"}
        }
    }
    
    with pytest.raises(ConfigValidationError) as exc_info:
        config.validate(schema)
        
    assert "invalid_number" in str(exc_info.value)
    assert "port" in str(exc_info.value)