class ConfigException(Exception):
    """Base exception for all configuration errors."""
    pass

class ConfigValidationError(ConfigException):
    """Raised when configuration data fails schema validation."""
    pass

class ConfigLoaderError(ConfigException):
    """Raised when a configuration source can't be loaded."""
    pass