# -*- coding: utf-8 -*-
import platform
if platform.system() == "Windows":
    try:
        from pygobject_prebuilt_deps import import_pygobject_dll_module
        import_pygobject_dll_module()
    except ImportError:
        pass 

import cairo
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")

from gi.repository import Gdk, GdkPixbuf, GLib, Gtk, Pango, PangoCairo
