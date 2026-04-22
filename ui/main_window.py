import json
import os

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib

from db.database import get_data_dir
from ui.drag_handle import DragHandle
from ui.date_header import DateHeader
from ui.todo_list import TodoListSection
from ui.add_form import AddForm

_POS_FILE = os.path.join(get_data_dir(), "window_pos.json")


class MainWindow(Gtk.Window):
    def __init__(self, repo):
        super().__init__(title="Todo")
        self._repo = repo
        self._save_timeout = 0

        self.set_decorated(False)
        self.set_default_size(400, -1)
        self.set_resizable(True)
        self.set_skip_taskbar_hint(False)
        self.get_style_context().add_class("main-window")

        self.connect("delete-event", lambda w, e: w.hide() or True)
        self.connect("configure-event", self._on_configure)

        self._build_ui()
        self._restore_position()
        self.show_all()
        self.refresh_todos()

    def _build_ui(self):
        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(root)

        # Drag handle strip at the very top
        root.pack_start(DragHandle(), False, False, 0)

        # Date header
        self._date_header = DateHeader(
            on_date_change=self._on_date_change,
            on_close=self.hide,
        )
        root.pack_start(self._date_header, False, False, 0)

        root.pack_start(
            Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 0
        )

        # Body: pending list + completed expander, with a minimum height
        body = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        body.set_size_request(-1, 160)

        self._pending_list = TodoListSection(
            on_toggle=self._on_toggle,
            on_delete=self._on_delete,
            max_height=240,
        )
        body.pack_start(self._pending_list, True, True, 0)

        self._expander = Gtk.Expander()
        self._expander.get_style_context().add_class("completed-expander")
        self._expander.set_margin_start(8)
        self._expander.set_margin_end(8)
        self._expander.set_margin_top(4)
        self._expander.set_margin_bottom(4)

        self._completed_list = TodoListSection(
            on_toggle=self._on_toggle,
            on_delete=self._on_delete,
            max_height=140,
        )
        self._expander.add(self._completed_list)
        body.pack_start(self._expander, False, False, 0)

        root.pack_start(body, True, True, 0)

        root.pack_start(
            Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 0
        )

        self._add_form = AddForm(on_add=self._on_add)
        root.pack_start(self._add_form, False, False, 0)

    # ── Position persistence ──────────────────────────────────────────

    def _restore_position(self):
        display = Gdk.Display.get_default()
        monitor = display.get_primary_monitor() if display else None
        workarea = monitor.get_workarea() if monitor else None

        try:
            with open(_POS_FILE) as f:
                pos = json.load(f)
            x, y = pos["x"], pos["y"]
            # Clamp to workarea so a stale position can't hide the window
            if workarea:
                x = max(workarea.x, min(x, workarea.x + workarea.width - 50))
                y = max(workarea.y, min(y, workarea.y + workarea.height - 50))
            self.move(x, y)
            return
        except (FileNotFoundError, KeyError, ValueError):
            pass

        # Default: top-center, just below the GNOME panel
        if workarea:
            self.move(workarea.x + workarea.width // 2 - 200, workarea.y)

    def _on_configure(self, _win, _event):
        if self._save_timeout:
            GLib.source_remove(self._save_timeout)
        self._save_timeout = GLib.timeout_add(600, self._flush_position)

    def _flush_position(self):
        x, y = self.get_position()
        try:
            os.makedirs(os.path.dirname(_POS_FILE), exist_ok=True)
            with open(_POS_FILE, "w") as f:
                json.dump({"x": x, "y": y}, f)
        except OSError:
            pass
        self._save_timeout = 0
        return False

    # ── Todo operations ───────────────────────────────────────────────

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
        self.resize(400, 1)

    def _on_date_change(self, _date_str):
        self.refresh_todos()

    def _on_toggle(self, todo_id, checked):
        if checked:
            self._repo.complete_todo(todo_id)
        else:
            self._repo.uncomplete_todo(todo_id)
        self.refresh_todos()

    def _on_delete(self, todo_id):
        self._repo.delete_todo(todo_id)
        self.refresh_todos()

    def _on_add(self, text):
        current_date = self._date_header.get_date().isoformat()
        self._repo.add_todo(text, current_date)
        self.refresh_todos()
