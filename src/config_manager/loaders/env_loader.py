import os
import logging
from typing import Dict, Any, Union  # Add Union import here
from .base_loader import BaseLoader

logger = logging.getLogger(__name__)

class EnvLoader(BaseLoader):
    """Load configuration from environment variables."""
    
    def __init__(self, source: str):
        self.prefix = source
        
    @classmethod
    def can_load(cls, source: Union[str, dict]) -> bool:  # Now properly imported
        return isinstance(source, str) and source.startswith('env://')
        
    def load(self) -> Dict[str, Any]:
        prefix = self.prefix[6:]  # Remove 'env://'
        config = {}
        
        for key, value in os.environ.items():
            if key.startswith(prefix):
                config_key = key[len(prefix):].lower()
                config[config_key] = self._parse_value(value)
                
        return config
        
    def _parse_value(self, value: str) -> Any:
        """Convert environment variable strings to appropriate types."""
        try:
            return int(value)
        except ValueError:
            pass
            
        try:
            return float(value)
        except ValueError:
            pass
            
        if value.lower() in ('true', 'false'):
            return value.lower() == 'true'
            
        return value