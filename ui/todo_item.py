import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class TodoItem(Gtk.ListBoxRow):
    def __init__(self, todo: dict, on_toggle, on_delete):
        super().__init__()
        self.todo = todo
        self._on_toggle = on_toggle
        self._on_delete = on_delete

        self.get_style_context().add_class("todo-item")

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        box.set_margin_start(8)
        box.set_margin_end(8)
        box.set_margin_top(4)
        box.set_margin_bottom(4)

        self._check = Gtk.CheckButton()
        self._check.set_active(bool(todo["completed"]))
        self._check.get_style_context().add_class("todo-check")
        self._check.connect("toggled", self._handle_toggle)
        box.pack_start(self._check, False, False, 0)

        self._label = Gtk.Label(label=todo["text"])
        self._label.set_xalign(0)
        self._label.set_line_wrap(True)
        self._label.set_max_width_chars(35)
        if todo["completed"]:
            self._label.get_style_context().add_class("completed-text")
        box.pack_start(self._label, True, True, 0)

        delete_btn = Gtk.Button(label="×")
        delete_btn.get_style_context().add_class("delete-btn")
        delete_btn.set_relief(Gtk.ReliefStyle.NONE)
        delete_btn.connect("clicked", self._handle_delete)
        box.pack_end(delete_btn, False, False, 0)

        self.add(box)
        self.show_all()

    def _handle_toggle(self, check):
        self._on_toggle(self.todo["id"], check.get_active())

    def _handle_delete(self, _btn):
        self._on_delete(self.todo["id"])
