from importlib.metadata import version

__version__ = version("zip2addr-jp")

from .api import Zip2Addr, lookup  # re-export for convenience

__all__ = ["Zip2Addr", "lookup"]
