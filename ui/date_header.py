import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from datetime import date, timedelta


class DateHeader(Gtk.Box):
    def __init__(self, on_date_change, on_close):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self._on_date_change = on_date_change
        self._current_date = date.today()
        self.get_style_context().add_class("date-header")

        # Make header draggable
        self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.connect("button-press-event", self._on_drag)

        prev_btn = Gtk.Button(label="‹")
        prev_btn.get_style_context().add_class("nav-btn")
        prev_btn.set_relief(Gtk.ReliefStyle.NONE)
        prev_btn.connect("clicked", lambda _: self._shift(-1))
        self.pack_start(prev_btn, False, False, 0)

        self._date_btn = Gtk.Button()
        self._date_btn.get_style_context().add_class("date-btn")
        self._date_btn.set_relief(Gtk.ReliefStyle.NONE)
        self._date_btn.connect("clicked", self._show_calendar)
        self.pack_start(self._date_btn, True, True, 0)

        next_btn = Gtk.Button(label="›")
        next_btn.get_style_context().add_class("nav-btn")
        next_btn.set_relief(Gtk.ReliefStyle.NONE)
        next_btn.connect("clicked", lambda _: self._shift(1))
        self.pack_start(next_btn, False, False, 0)

        close_btn = Gtk.Button(label="×")
        close_btn.get_style_context().add_class("close-btn")
        close_btn.set_relief(Gtk.ReliefStyle.NONE)
        close_btn.connect("clicked", lambda _: on_close())
        self.pack_end(close_btn, False, False, 0)

        self._popover = self._build_calendar_popover()
        self._update_label()

    def _build_calendar_popover(self):
        popover = Gtk.Popover()
        popover.set_relative_to(self._date_btn)

        self._calendar = Gtk.Calendar()
        self._calendar.connect("day-selected-double-click", self._on_calendar_select)
        self._calendar.connect("day-selected", self._on_calendar_select)
        popover.add(self._calendar)
        self._calendar.show()
        return popover

    def _show_calendar(self, _btn):
        d = self._current_date
        self._calendar.select_month(d.month - 1, d.year)
        self._calendar.select_day(d.day)
        self._popover.popup()

    def _on_calendar_select(self, cal):
        year, month, day = cal.get_date()
        self.set_date(date(year, month + 1, day))
        self._popover.popdown()

    def _shift(self, delta: int):
        self.set_date(self._current_date + timedelta(days=delta))

    def set_date(self, new_date: date):
        self._current_date = new_date
        self._update_label()
        self._on_date_change(new_date.isoformat())

    def get_date(self) -> date:
        return self._current_date

    def _update_label(self):
        today = date.today()
        d = self._current_date
        if d == today:
            label = f"Today — {d.strftime('%a, %b %-d')}"
        elif d == today - timedelta(days=1):
            label = f"Yesterday — {d.strftime('%a, %b %-d')}"
        elif d == today + timedelta(days=1):
            label = f"Tomorrow — {d.strftime('%a, %b %-d')}"
        else:
            label = d.strftime("%A, %b %-d %Y")
        self._date_btn.set_label(label)

    def _on_drag(self, widget, event):
        if event.button == Gdk.BUTTON_PRIMARY:
            win = widget.get_toplevel()
            win.begin_move_drag(
                event.button,
                int(event.x_root),
                int(event.y_root),
                event.time,
            )
