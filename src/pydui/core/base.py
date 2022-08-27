from enum import Enum


class PyDuiLayoutEnum(Enum):
    """Layout type enum

    Attributes:
        Undefine: default
        HLayout: horizontal layout
        VLayout: vertical layout

    """

    NotLayout = 0
    HLayout = 1
    VLayout = 2
    FitLayout = 3
    FixedLayout = 4
    CustomLayout = 10
