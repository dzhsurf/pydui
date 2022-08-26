"""Utils function
"""

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


def Str2Size(text: str) -> tuple[int, int]:
    """Convert text to tuple[int, int]

    if the text in wrong format, it will return (0, 0)

    Args:
        text (str): input text

    Retruns:
        tuple[int, int]: return size in tuple
    """
    arr = text.split(",")
    if len(arr) != 2:
        return (0, 0)

    return (int(arr[0]), int(arr[1]))


def Str2Position(text: str) -> Gtk.WindowPosition:
    """Convert text to Gtk.WindowPosition flag

    if the input not match, it will return Gtk.WindowPosition.CENTER by default.

    Args:
        text (str): input text

    Retruns:
        Gtk.WindowPosition: return gtk position flag
    """
    flags_table = {
        "CENTER": Gtk.WindowPosition.CENTER,
    }
    if text in flags_table:
        return flags_table[text]

    return Gtk.WindowPosition.CENTER
