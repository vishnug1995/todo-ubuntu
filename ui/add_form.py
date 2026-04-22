import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


class AddForm(Gtk.Box):
    def __init__(self, on_add):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self._on_add = on_add
        self.get_style_context().add_class("add-form")
        self.set_margin_start(8)
        self.set_margin_end(8)
        self.set_margin_top(6)
        self.set_margin_bottom(8)

        self._entry = Gtk.Entry()
        self._entry.set_placeholder_text("Add a task…")
        self._entry.get_style_context().add_class("add-entry")
        self._entry.connect("activate", self._handle_add)
        self.pack_start(self._entry, True, True, 0)

        add_btn = Gtk.Button(label="Add")
        add_btn.get_style_context().add_class("add-btn")
        add_btn.connect("clicked", self._handle_add)
        self.pack_start(add_btn, False, False, 0)

    def _handle_add(self, _widget):
        text = self._entry.get_text().strip()
        if text:
            self._on_add(text)
            self._entry.set_text("")

    def focus_entry(self):
        self._entry.grab_focus()
