import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from ui.todo_item import TodoItem


class TodoListSection(Gtk.Box):
    """Scrollable ListBox section for either pending or completed todos."""

    def __init__(self, on_toggle, on_delete, max_height: int = 260):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self._on_toggle = on_toggle
        self._on_delete = on_delete

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_max_content_height(max_height)
        scrolled.set_propagate_natural_height(True)

        self._listbox = Gtk.ListBox()
        self._listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self._listbox.get_style_context().add_class("todo-listbox")
        scrolled.add(self._listbox)

        self.pack_start(scrolled, True, True, 0)

    def populate(self, todos: list[dict]):
        for child in self._listbox.get_children():
            self._listbox.remove(child)
        for todo in todos:
            item = TodoItem(todo, self._on_toggle, self._on_delete)
            self._listbox.add(item)
        self._listbox.show_all()

    def count(self) -> int:
        return len(self._listbox.get_children())
