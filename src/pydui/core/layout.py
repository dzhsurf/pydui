# layout.py
from dataclasses import dataclass

from pydui.core.widget import *


class PyDuiLayout(PyDuiWidget):

    """Layout base class, all layouts inherit from PyDuiLayout"""

    __children: list[PyDuiWidget]
    __children_id_dict: dict[str, PyDuiWidget]

    def __init__(self):
        super().__init__()
        self.__children = []
        self.__children_id_dict = {}

    def get_child(self, widget_id: str) -> Optional[PyDuiWidget]:
        """Get child widget by widget_id

        Args:
            widget_id (str): widget id

        Returns:
            PyDuiWidget: return widget object.
        """
        if widget_id in self.__children_id_dict:
            return self.__children_id_dict[widget_id]
        return None

    def get_child_at(self, index: int) -> Optional[PyDuiWidget]:
        """Get child widget at index

        if the index overbound, it will return None.

        Args:
            index (int): child index

        Returns:
            PyDuiWidget: return widget object.
        """
        if index < 0 or index >= len(self.__children):
            return None
        return self.__children[index]

    def add_child(self, child: PyDuiWidget):
        """Add child widget.

        if child has been added, ignore.

        Args:
            child (PyDuiWidget): child widget

        """
        if (child is None) or (self.get_child(child.get_id()) is not None):
            return

        self.__children.append(child)
        widget_id = child.get_id()
        if len(widget_id) > 0 and (widget_id not in self.__children_id_dict):
            self.__children_dict[widget_id] = child
        gtk_widget = self.get_gtk_widget()
        if gtk_widget is not None and child.get_gtk_widget() is not None:
            gtk_widget.add(child.get_gtk_widget())

    def add_child_at(self, child: PyDuiWidget, index: int):
        """Add child widget at index

        if the index overbound, it will add widget to last position.

        Args:
            child (PyDuiWidget): child widget
            index (int): target index

        Returns:
            PyDuiWidget: return widget object.
        """
        pass

    def remove_child(self, widget_id: str):
        """Remove child widget by widget_id

        Args:
            widget_id (str): widget id

        """
        pass

    def remove_child_at(self, index: int):
        """Remove child widget at index

        if the index overbound, do nothing.

        Args:
            index (int): widget index

        """
        pass

    @property
    def child_count(self) -> int:
        """Return child count

        Returns:
            int: return child widget count.
        """
        pass

    @property
    def inset(self) -> tuple[int, int, int, int]:
        """Return widget inset

        The value in tuple means [left, top, right, bottom]

        Returns:
            tuple[int, int, int, int]: return inset.
        """
        pass

    @inset.setter
    def inset(self, inset: tuple[int, int, int, int]):
        """Set the widget inset

        Args:
            inset (tuple[int, int, int, int]): widget inset

        """
        pass

    # private function
    def __do_layout__(self):
        pass
