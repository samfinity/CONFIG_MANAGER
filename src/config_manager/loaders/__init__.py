from .base_loader import BaseLoader
from .json_loader import JsonLoader, DictLoader
from .env_loader import EnvLoader

class LoaderRegistry:
    """Registry for configuration loaders."""
    
    def __init__(self):
        self._loaders = [JsonLoader, DictLoader, EnvLoader]
        
    def get_loader(self, source: any) -> BaseLoader:
        """Find appropriate loader for the given source."""
        for loader in self._loaders:
            if loader.can_load(source):
                return loader(source)
        return None