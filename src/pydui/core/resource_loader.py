# -*- coding: utf-8 -*-
"""Resource Loader Module"""
import logging
import os
import pathlib
from abc import ABC, abstractmethod
from typing import Tuple


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
    def load_image(self, path: str) -> Tuple[bytes, float]:
        """Load image buffer with hi-dpi suppose"""
        pass

    @abstractmethod
    def load_string(self, id: str) -> str:
        """Load intl language text by text id"""
        pass


class __PyDuiDefaultResourceLoader__(PyDuiResourceLoader):
    def __init__(self):
        super().__init__()

    def __is_macosx_app__(self) -> bool:
        if "GTK_PATH" in os.environ and os.environ["GTK_PATH"].endswith(".app/Contents/MacOS"):
            return True
        return False

    def __get_macosx_res_dir__(self) -> pathlib.Path:
        return pathlib.Path(os.environ["GTK_PATH"]).joinpath("../Resources")

    def resource_path(self, relative: str) -> str:
        # syslog.syslog(syslog.LOG_ALERT, str(os.environ))
        if self.__is_macosx_app__():
            # RUN from Mac app
            res_path = self.__get_macosx_res_dir__()
            return str(res_path.joinpath(relative))
        else:
            return relative

    def scheme(self) -> str:
        return "__default__"

    def load_xml(self, path: str) -> str:
        content = ""
        res_path = self.resource_path(path)
        try:
            with open(res_path, "r") as f:
                content = f.read()
                return content
        except:
            logging.error(f"open path fail. path = {res_path}")
            # syslog.syslog(syslog.LOG_ALERT, f"open path fail. path = {res_path}")
        return content

    def load_image(self, path: str) -> Tuple[bytes, float]:
        image_ext = pathlib.Path(path).suffix
        image_path = path.removesuffix(image_ext)
        # try to match the dpi resource
        for op in [("@2x", 2.0), ("", 1.0)]:
            filename = f"{image_path}{op[0]}{image_ext}"
            buf = self.load_data(filename)
            if len(buf) > 0:
                return (buf, op[1])
        return (bytes(), 1.0)

    def load_data(self, path: str) -> bytes:
        try:
            res_path = self.resource_path(path)
            with open(res_path, "rb") as f:
                buf = f.read()
                return buf
        except:
            logging.error(f"open path fail. path = {res_path}")
            # syslog.syslog(syslog.LOG_ALERT, f"open path fail. path = {res_path}")
        return bytes()

    def load_string(self, id: str) -> str:
        return ""


def create_default_resource_loader() -> PyDuiResourceLoader:
    return __PyDuiDefaultResourceLoader__()
