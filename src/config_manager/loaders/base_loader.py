from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, Union

class BaseLoader(ABC):
    """Abstract base class for configuration loaders."""
    
    @classmethod
    @abstractmethod
    def can_load(cls, source: Union[str, dict]) -> bool:
        """Check if this loader can handle the given source."""
        pass
        
    @abstractmethod
    def load(self) -> Dict[str, Any]:
        """Load configuration from source."""
        pass