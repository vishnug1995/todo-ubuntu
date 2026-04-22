#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "==> Installing system dependencies..."
sudo apt-get install -y python3-gi python3-gi-cairo gir1.2-gtk-3.0

# Fill in the real install path in the .desktop file
DESKTOP_CONTENT=$(sed "s|INSTALL_PATH|$SCRIPT_DIR|g" "$SCRIPT_DIR/todo-ubuntu.desktop")

echo "==> Registering app in launcher (Activities / app grid)..."
APPS_DIR="$HOME/.local/share/applications"
mkdir -p "$APPS_DIR"
echo "$DESKTOP_CONTENT" > "$APPS_DIR/todo-ubuntu.desktop"
chmod 644 "$APPS_DIR/todo-ubuntu.desktop"
# Refresh GNOME's app database so it appears immediately
update-desktop-database "$APPS_DIR" 2>/dev/null || true

echo "==> Setting up autostart on login..."
AUTOSTART_DIR="$HOME/.config/autostart"
mkdir -p "$AUTOSTART_DIR"
echo "$DESKTOP_CONTENT" > "$AUTOSTART_DIR/todo-ubuntu.desktop"
chmod 644 "$AUTOSTART_DIR/todo-ubuntu.desktop"

echo ""
echo "All done!"
echo ""
echo "Launch now:     python3 $SCRIPT_DIR/todo_app.py"
echo "Or search:      Press the Super key, type 'Todo'"
echo "Pin to dock:    Right-click the app icon → Add to Favorites"
echo ""
echo "The app will also open automatically on every login."
