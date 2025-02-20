
import importlib.metadata

if not __package__:
    __version__ = "0.0.0"
else:
    __version__ = importlib.metadata.version(__package__)