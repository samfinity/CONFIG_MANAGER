import os
import pytest
from config_manager.loaders.env_loader import EnvLoader

def test_env_loader(monkeypatch):
    # Set up environment variables
    monkeypatch.setenv("APP_DB_HOST", "env_host")
    monkeypatch.setenv("APP_DB_PORT", "3308")
    
    # Initialize the EnvLoader with the proper prefix
    loader = EnvLoader("env://APP_")
    config_data = loader.load()
    
    # The loader lowercases the remaining key names.
    assert "db_host" in config_data
    assert config_data["db_host"] == "env_host"
    assert "db_port" in config_data
    assert config_data["db_port"] == 3308