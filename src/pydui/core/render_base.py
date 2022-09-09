# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Any

from pydui.core.import_gtk import *
from pydui.core.resource_loader import PyDuiResourceLoader


class PyDuiRenderManagerBase(ABC):
    @abstractmethod
    def get_resource_loader(self) -> PyDuiResourceLoader:
        pass

    @abstractmethod
    def notify_redraw(self):
        pass

    @abstractmethod
    def get_render_context(self) -> cairo.Context:
        pass

    @abstractmethod
    def cancel_task(self, task_id: str):
        pass

    @abstractmethod
    def post_task(self, fn: callable, *args: Any, **kwargs: Any):
        pass

    @abstractmethod
    def post_task_with_delay(self, delay: float, fn: callable, *args: Any, **kwargs: Any):
        pass
