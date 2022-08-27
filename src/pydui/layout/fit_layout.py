"""FitLayout unit
"""

from pydui.core.layout import *
from pydui.core.widget import *


class PyDuiFitLayout(PyDuiLayout):
    """FitLayout implement"""

    def __init__(self, parent: PyDuiWidget):
        super().__init__(parent, PyDuiLayoutEnum.FitLayout)
