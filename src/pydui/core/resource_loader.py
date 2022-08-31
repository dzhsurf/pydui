"""Resource Loader Module"""
import logging
from abc import ABC, abstractmethod


class PyDuiResourceLoader(ABC):
    """PyDuiResourceLoader"""

    @abstractmethod
    def scheme(self) -> str:
        """Return loader scheme"""
        pass

    @abstractmethod
    def load_xml(self, path: str) -> str:
        """Load xml layout file"""
        pass

    @abstractmethod
    def load_data(self, path: str) -> bytes:
        """Load data"""
        pass

    @abstractmethod
    def load_string(self, id: str) -> str:
        """Load intl language text by text id"""
        pass


class __PyDuiDefaultResourceLoader__(PyDuiResourceLoader):
    def __init__(self):
        pass

    def scheme(self) -> str:
        return "__default__"

    def load_xml(self, path: str) -> str:
        content = ""
        try:
            f = open(path, "r")
            content = f.read()
            f.close()
        except:
            logging.error(f"open path fail. path = {path}")
        return content

    def load_data(self, path: str) -> bytes:
        return bytes()

    def load_string(self, id: str) -> str:
        return ""


def create_default_resource_loader() -> PyDuiResourceLoader:
    return __PyDuiDefaultResourceLoader__()
