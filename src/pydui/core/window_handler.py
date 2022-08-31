from __future__ import annotations

from pydui.core.resource_loader import PyDuiResourceLoader


class PyDuiWindowHandler(object):

    """Window handler"""

    def on_window_init(self, window: PyDuiWindow):
        """On window init event"""
        pass

    def on_window_destroy(self):
        """On window destroy event"""
        pass

    def on_window_position_changed(self, x: float, y: float):
        """On window position changed event

        Args:
            x (float): x coordinate
            y (float): y coordinate
        """
        pass

    def on_window_size_changed(self, w: float, h: float):
        """On window size changed event

        Args:
            w (float): window width
            h (float): window height
        """
        pass

    def on_window_visible_changed(self, show: bool):
        """On window visible changed event

        Args:
            show: window is visible
        """
        pass
