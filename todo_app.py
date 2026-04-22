#!/usr/bin/env python3
import logging
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Gio

from db.database import create_repository, get_data_dir
from ui.main_window import MainWindow

# Log errors to file so failures are visible even when launched from icon
_log_path = os.path.join(get_data_dir(), "app.log")
logging.basicConfig(
    filename=_log_path,
    level=logging.ERROR,
    format="%(asctime)s %(levelname)s: %(message)s",
)


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


class TodoApp(Gtk.Application):
    def __init__(self):
        super().__init__(
            application_id="com.personal.todo-ubuntu",
            flags=Gio.ApplicationFlags.FLAGS_NONE,
        )
        self._repo = None
        self._window = None

    def do_startup(self):
        Gtk.Application.do_startup(self)
        try:
            load_styles()
            self._repo = create_repository()
        except Exception:
            logging.exception("Startup failed")
            raise

    def do_activate(self):
        # Called on every launch attempt — including from a second instance.
        # If a window already exists (app was hidden), just show it again.
        if self._repo is None:
            return  # startup failed; error already logged
        try:
            if self._window is None:
                self._window = MainWindow(self._repo)
                self._window.set_application(self)
            self._window.present()
        except Exception:
            logging.exception("Activate failed")
            raise


def main():
    app = TodoApp()
    sys.exit(app.run(sys.argv))


if __name__ == "__main__":
    main()
