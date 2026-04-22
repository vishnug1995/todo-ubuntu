import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


class DragHandle(Gtk.EventBox):
    """Thin grip strip at the top of the window — click-drag to move."""

    def __init__(self):
        super().__init__()
        self.get_style_context().add_class("drag-handle")
        self.set_size_request(-1, 16)

        grip = Gtk.Label(label="· · · · ·")
        grip.get_style_context().add_class("drag-grip")
        self.add(grip)

        self.add_events(
            Gdk.EventMask.BUTTON_PRESS_MASK | Gdk.EventMask.ENTER_NOTIFY_MASK
        )
        self.connect("button-press-event", self._on_press)
        self.connect("realize", self._set_cursor)

    def _set_cursor(self, widget):
        cursor = Gdk.Cursor.new_from_name(widget.get_display(), "grab")
        if widget.get_window():
            widget.get_window().set_cursor(cursor)

    def _on_press(self, widget, event):
        if event.button == Gdk.BUTTON_PRIMARY:
            win = widget.get_toplevel()
            win.begin_move_drag(
                event.button,
                int(event.x_root),
                int(event.y_root),
                event.time,
            )
