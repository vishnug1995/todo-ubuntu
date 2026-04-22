# Todo Ubuntu

A lightweight personal todo widget for Ubuntu desktop. Sits as a compact panel at the top of your screen — always visible, no clutter.


## Features

- Compact frameless panel pinned to the top-center of your screen
- Date navigation — step through days or pick any date from a calendar
- Checkbox to complete todos; completed items collapse into a separate section
- Todos are stored locally per date — each day has its own list
- Persists across restarts (SQLite at `~/.config/todo-ubuntu/todos.db`)
- Auto-starts on login via `~/.config/autostart/`
- Drag the header to reposition the panel anywhere on screen

## Stack

| Layer | Technology |
|---|---|
| UI | Python 3 + GTK 3 (PyGObject) |
| Storage | SQLite via Python stdlib `sqlite3` |
| Styling | GTK CSS (Catppuccin dark theme) |

No npm, no Electron, no heavy runtime — just Python and system GTK libraries (~5 MB footprint).

## Installation

### Prerequisites

Ubuntu 20.04 or later with a GNOME/GTK desktop environment.

### Setup

```bash
git clone https://github.com/vishnug1995/todo-ubuntu.git
cd todo-ubuntu
bash setup.sh
```

`setup.sh` will:
1. Install GTK Python bindings (`python3-gi`, `python3-gi-cairo`, `gir1.2-gtk-3.0`) via `apt`
2. Register the app in `~/.local/share/applications/` so it appears in the GNOME Activities launcher
3. Write `~/.config/autostart/todo-ubuntu.desktop` so the app opens on every login

### Launch

**From the app launcher (recommended):**
Press the **Super** key, type **"Todo"** — the app appears. Right-click its icon → **Add to Favorites** to pin it to your dock.

**From terminal:**
```bash
python3 todo_app.py
```

The widget appears at the top-center of your primary monitor. It will also open automatically on your next login.

## Usage

| Action | How |
|---|---|
| Add a todo | Type in the bottom input and press **Enter** or click **Add** |
| Complete a todo | Click the checkbox — it moves to the Completed section |
| Undo completion | Click the checkbox again in the Completed section |
| Delete a todo | Hover over a row and click the **×** button that appears |
| Change date | Click **‹** / **›** to step days, or click the date label for a calendar picker |
| Move the panel | Click and drag the date header bar |
| Hide the panel | Click the **×** in the top-right corner (app keeps running) |

## Project Structure

```
todo-ubuntu/
├── todo_app.py           # Entry point — loads styles, creates repo + window
├── style.css             # GTK CSS (Catppuccin Mocha dark theme)
├── setup.sh              # One-time install: apt deps + autostart .desktop
├── todo-ubuntu.desktop   # Autostart template
├── db/
│   ├── database.py       # SQLite init, schema migrations, repository factory
│   └── repository.py     # Abstract TodoRepository + SqliteRepository
└── ui/
    ├── main_window.py    # Frameless GTK window, top-pinned, assembles layout
    ├── date_header.py    # Date label, prev/next buttons, calendar popover
    ├── todo_list.py      # Scrollable ListBox section (pending / completed)
    ├── todo_item.py      # Single todo row: checkbox + label + delete button
    └── add_form.py       # Text entry + Add button
```

## Data Storage

Todos are stored in a SQLite database at:

```
~/.config/todo-ubuntu/todos.db
```

Schema:

```sql
CREATE TABLE todos (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    text         TEXT    NOT NULL,
    date         TEXT    NOT NULL,   -- 'YYYY-MM-DD'
    completed    INTEGER NOT NULL DEFAULT 0,
    created_at   TEXT    NOT NULL DEFAULT (datetime('now')),
    completed_at TEXT
);
```

## Future: Supabase Integration

The storage layer uses an abstract `TodoRepository` base class (`db/repository.py`). To add Supabase:

1. Create `db/supabase_repository.py` implementing the same 5-method interface
2. Install `supabase-py`: `pip install supabase`
3. In `db/database.py`, update `create_repository()` to return a `SupabaseRepository` when `SUPABASE_URL` is set

No UI code needs to change.

## Uninstall

Remove the launcher entry and autostart:

```bash
rm ~/.config/autostart/todo-ubuntu.desktop
rm ~/.local/share/applications/todo-ubuntu.desktop
update-desktop-database ~/.local/share/applications
```
