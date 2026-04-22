import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

from ui.date_header import DateHeader
from ui.todo_list import TodoListSection
from ui.add_form import AddForm


class MainWindow(Gtk.Window):
    def __init__(self, repo):
        super().__init__(title="Todo")
        self._repo = repo

        self.set_decorated(False)
        self.set_default_size(400, -1)
        self.set_resizable(True)
        self.set_skip_taskbar_hint(False)
        self.get_style_context().add_class("main-window")

        # Prevent actual destroy; just hide
        self.connect("delete-event", lambda w, e: w.hide() or True)

        self._build_ui()
        self._position_window()
        self.show_all()
        self.refresh_todos()

    def _build_ui(self):
        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(root)

        # Date header (draggable)
        self._date_header = DateHeader(
            on_date_change=self._on_date_change,
            on_close=self.hide,
        )
        root.pack_start(self._date_header, False, False, 0)

        sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        root.pack_start(sep, False, False, 0)

        # Pending todos
        self._pending_list = TodoListSection(
            on_toggle=self._on_toggle,
            on_delete=self._on_delete,
            max_height=260,
        )
        root.pack_start(self._pending_list, False, False, 0)

        # Completed expander
        self._expander = Gtk.Expander()
        self._expander.get_style_context().add_class("completed-expander")
        self._expander.set_margin_start(8)
        self._expander.set_margin_end(8)
        self._expander.set_margin_top(4)

        self._completed_list = TodoListSection(
            on_toggle=self._on_toggle,
            on_delete=self._on_delete,
            max_height=160,
        )
        self._expander.add(self._completed_list)
        root.pack_start(self._expander, False, False, 0)

        sep2 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        root.pack_start(sep2, False, False, 0)

        # Add form
        self._add_form = AddForm(on_add=self._on_add)
        root.pack_start(self._add_form, False, False, 0)

    def _position_window(self):
        display = Gdk.Display.get_default()
        monitor = display.get_primary_monitor()
        if monitor:
            geom = monitor.get_geometry()
            self.move(geom.x + geom.width // 2 - 200, geom.y)

    def refresh_todos(self):
        current_date = self._date_header.get_date().isoformat()
        todos = self._repo.get_todos_for_date(current_date)

        pending = [t for t in todos if not t["completed"]]
        completed = [t for t in todos if t["completed"]]

        self._pending_list.populate(pending)
        self._completed_list.populate(completed)

        n = len(completed)
        self._expander.set_label(f"Completed ({n})" if n else "Completed")
        self._expander.set_sensitive(n > 0)

        self.show_all()
        self.resize(400, 1)  # shrink to fit content

    def _on_date_change(self, _date_str: str):
        self.refresh_todos()

    def _on_toggle(self, todo_id: int, checked: bool):
        if checked:
            self._repo.complete_todo(todo_id)
        else:
            self._repo.uncomplete_todo(todo_id)
        self.refresh_todos()

    def _on_delete(self, todo_id: int):
        self._repo.delete_todo(todo_id)
        self.refresh_todos()

    def _on_add(self, text: str):
        current_date = self._date_header.get_date().isoformat()
        self._repo.add_todo(text, current_date)
        self.refresh_todos()
