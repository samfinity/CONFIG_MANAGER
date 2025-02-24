# Config Manager

Config Manager is a Python library designed to load, merge, and validate configuration settings from multiple sources (dictionaries, JSON files, YAML files, and environment variables). It provides a simple API to retrieve nested configuration values using dot-notation and enforces the configuration structure using JSON Schema.

## Features

- **Multiple Configuration Sources:** Combine settings from in-code dictionaries, JSON files, YAML files, or environment variables.
- **Priority-Based Merging:** Later-loaded sources override values from earlier ones.
- **Schema Validation:** Validate the configuration against a JSON Schema and enforce no additional properties.
- **Dot-Notation Access:** Retrieve nested values easily with dot-separated keys.

## Installation

To install the project in editable mode (recommended for development), run:

```bash
python -m pip install -e .[dev]
```

The `[dev]` extra installs development dependencies such as pytest, black, flake8, etc.

## Usage

### Example 1: Loading and Merging Configurations

```python
from config_manager import ConfigManager

# Initialize the ConfigManager
config = ConfigManager()

# Load configurations from different sources:
# 1. A Python dictionary
# 2. A JSON file (make sure the file exists on this path)
# 3. Environment variables with a prefix "APP_"
config.load_configs([
    {"database": {"host": "localhost", "port": 5432}},
    "src/config_manager/configs/config.json",
    "env://APP_"
])

# Access configuration values using dot-notation:
db_host = config.get("database.host")
db_port = config.get("database.port")
print("Database Host:", db_host)
print("Database Port:", db_port)
```

### Example 2: Using Environment Variables

Set environment variables before running your code. For example, on Windows Command Prompt:

```cmd
set APP_DB_HOST=env_host
set APP_DB_PORT=3308
```

In Python, load and access them as follows:

```python
from config_manager import ConfigManager

config = ConfigManager()
config.load_configs(["env://APP_"])

print("Environment DB Host:", config.get("db.host"))
print("Environment DB Port:", config.get("db.port"))
```

### Example 3: Configuration Files

Create configuration files in JSON or YAML and store them under `src/config_manager/configs/`.

#### JSON Example (`src/config_manager/configs/config.json`)

```json
{
    "database": {
        "host": "json_host",
        "port": 3306
    }
}
```

#### YAML Example (`src/config_manager/configs/config.yaml`)

```yaml
database:
  host: "yaml_host"
  port: 3307
```

Test merging these configurations with in-code dictionaries:

```python
config = ConfigManager()
config.load_configs([
    "src/config_manager/configs/config.yaml",
    {"database": {"host": "override_host"}}
])
# The final configuration should have 'override_host' for database.host
print("Merged DB Host:", config.get("database.host"))
print("Merged DB Port:", config.get("database.port"))
```

### Example 4: Schema Validation

Define a JSON Schema and validate the configuration:

```python
from config_manager import ConfigManager
from config_manager.exceptions import ConfigValidationError

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
config.load_configs([
    {"database": {"host": "localhost", "port": 5432}}
])

try:
    config.validate(schema)
    print("Configuration is valid!")
except ConfigValidationError as e:
    print("Configuration validation error:", e)
```

If the configuration doesn't match the schema (for example, if an extra key is provided or a value is of the wrong type), a `ConfigValidationError` will be raised with details about the error.

## Running Tests

We use `pytest` for unit tests. To run the tests, execute the following command from the project root:

pytest -v

