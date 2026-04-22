#!/usr/bin/env python3
import os
import sys

# Allow imports from project root
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

from db.database import create_repository
from ui.main_window import MainWindow


def load_styles():
    css_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "style.css")
    if not os.path.exists(css_path):
        return
    provider = Gtk.CssProvider()
    provider.load_from_path(css_path)
    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(),
        provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
    )


def main():
    load_styles()
    repo = create_repository()
    win = MainWindow(repo)
    win.connect("destroy", Gtk.main_quit)
    Gtk.main()


if __name__ == "__main__":
    main()
