# -*- coding: utf-8 -*-
import weakref
from abc import abstractmethod
from typing import Protocol
from weakref import ReferenceType

from pydui.core.widget import PyDuiWidget
from pydui.layout.pglayout import PyDuiLayoutWithPogaSupport
from pydui.layout.scrolled_layout import PyDuiScrolledLayout


class PyDuiListNode:
    pass


class PyDuiListViewDataSource(Protocol):
    @abstractmethod
    def item_count(self) -> int:
        pass

    @abstractmethod
    def item_node(self, index: int) -> PyDuiListNode:
        pass


class PyDuiListViewDelegate(Protocol):
    @abstractmethod
    def item_height(self, index: int) -> float:
        pass

    @abstractmethod
    def create_item_by_node(self, index: int, node: PyDuiListNode) -> PyDuiWidget:
        pass


class PyDuiListView(PyDuiLayoutWithPogaSupport):
    """PyDuiListView"""

    __body: PyDuiScrolledLayout = None
    __datasource: ReferenceType[PyDuiListViewDataSource] = None

    @staticmethod
    def build_name() -> str:
        return "ListView"

    def __init__(self):
        super().__init__()
        self.__body = PyDuiScrolledLayout()
        self.__body.enable_vscroll = True
        super().add_child(self.__body)

    def set_datasource(self, datasource: PyDuiListViewDataSource):
        self.__datasource = weakref.ref(datasource)
        self.reload()

    def reload(self):
        if self.__datasource is None:
            return
        # self.__datasource.reload()

    def add_child(self, child: PyDuiWidget):
        raise ValueError("ListView widget not support add_child.")
        return super().add_child(child)

    def add_child_at(self, child: PyDuiWidget, index: int):
        raise ValueError("ListView widget not support add_child_at.")
        return super().add_child_at(child, index)

    def remove_child(self, child: PyDuiWidget):
        raise ValueError("ListView widget not support remove_child.")
        return super().remove_child(child)

    def remove_child_at(self, index: int):
        raise ValueError("ListView widget not support remove_child_at.")
        return super().remove_child_at(index)

    def remove_child_by_id(self, widget_id: str):
        raise ValueError("ListView widget not support remove_child_by_id.")
        return super().remove_child_by_id(widget_id)
