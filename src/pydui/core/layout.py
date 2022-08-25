# layout.py
from dataclasses import dataclass

from pydui.core.widget import *

class PyDuiLayout(PyDuiWidget):
    def __init__(self):
        pass

    def get_child(self, widget_id: str) -> Optional[PyDuiWidget]:
        pass

    def get_child_at(self, index: int) -> Optional[PyDuiWidget]:
        pass

    def add_child(self, child: PyDuiWidget):
        pass

    def add_child_at(self, child: PyDuiWidget, index: int):
        pass

    def remove_child(self, widget_id: str):
        pass

    def remove_child_at(self, index: int):
        pass

    @property
    def child_count(self) -> int:
        pass

    @property
    def inset(self) -> tuple[int, int, int, int]:
        pass

    @inset.setter
    def inset(self, inset: tuple[int, int, int, int]):
        pass

    # private function
    def __do_layout__(self):
        pass
