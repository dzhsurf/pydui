# -*- coding: utf-8 -*-
import platform


class PyDuiScreen:
    """PyDuiScreen class"""

    @staticmethod
    def get_system_dpi_scale() -> float:
        """Return system dpi scale"""
        # TODO: detect system dpi scale
        if platform.system() == "Windows":
            # if platform.release() == "7":
            #     ctypes.windll.user32.SetProcessDPIAware()
            # elif platform.release() == "8" or platform.release() == "10":
            #     ctypes.windll.shcore.SetProcessDpiAwareness(1)
            return 2.0
        elif platform.system() == "Linux":
            pass
        elif platform.system() == "Darwin":
            pass
        return 2.0
