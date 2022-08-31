from dataclasses import dataclass
from typing import Optional, Type

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from pydui.core import utils
from pydui.core.layout import *
from pydui.core.widget import *
from pydui.widgets.label import *


class PyDuiButton(PyDuiLabel):

    """Label widget"""

    def __init__(self, parent: PyDuiWidget):
        super().__init__(parent)
