# -*- coding: utf-8 -*-
import cairo  # type: ignore
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")

from gi.repository import Gdk, GdkPixbuf, GLib, Gtk, Pango, PangoCairo  # type: ignore
