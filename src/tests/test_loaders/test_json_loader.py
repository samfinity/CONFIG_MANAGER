
import json
from pathlib import Path
import pytest
from config_manager.loaders.json_loader import JsonLoader

def test_json_loader(tmp_path):
    # Create a temporary JSON file with sample configuration data.
    data = {
        "database": {
            "host": "json_test_host",
            "port": 1234
        }
    }
    file_path = tmp_path / "config.json"
    file_path.write_text(json.dumps(data))
    
    # Initialize the JsonLoader with the temporary file path.
    loader = JsonLoader(str(file_path))
    loaded_config = loader.load()
    
    assert "database" in loaded_config
    assert loaded_config["database"]["host"] == "json_test_host"
    assert loaded_config["database"]["port"] == 1234