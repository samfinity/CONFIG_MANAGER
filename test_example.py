from config_manager import ConfigManager

# Initialize the ConfigManager
config = ConfigManager()

# Load configurations from different sources:
# 1. A Python dictionary
# 2. A JSON file (make sure the file exists on this path)
# 3. Environment variables with a prefix "APP_"
config.load_configs([
    "src/config_manager/configs/config.json",
    {"database": {"host": "localhost", "port": 5432}},
    "env://APP_"
])

# Access configuration values using dot-notation:
db_host = config.get("database.host")
db_port = config.get("database.port")
print("Database Host:", db_host)
print("Database Port:", db_port)

