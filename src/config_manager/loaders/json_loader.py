import json
import logging
from pathlib import Path
from typing import Dict, Any, Union
from .base_loader import BaseLoader

logger = logging.getLogger(__name__)

class JsonLoader(BaseLoader):
    """Configuration loader for JSON files."""
    
    def __init__(self, source: str):
        self.file_path = Path(source)
        
    @classmethod
    def can_load(cls, source: Union[str, dict]) -> bool:
        if isinstance(source, str):
            return source.endswith('.json') and Path(source).is_file()
        return False
        
    def load(self) -> Dict[str, Any]:
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            logger.error(f"Failed to load JSON from {self.file_path}: {e}")
            raise

class DictLoader(BaseLoader):
    """Loader for Python dictionaries."""
    
    @classmethod
    def can_load(cls, source: Union[str, dict]) -> bool:
        return isinstance(source, dict)
        
    def __init__(self, source: dict):
        self.config_dict = source
        
    def load(self) -> Dict[str, Any]:
        return self.config_dict.copy()