# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

from pydui.core.resource_loader import PyDuiResourceLoader


class PyDuiRenderManagerBase(ABC):
    @abstractmethod
    def get_resource_loader(self) -> PyDuiResourceLoader:
        pass

    @abstractmethod
    def notify_redraw(self):
        pass
