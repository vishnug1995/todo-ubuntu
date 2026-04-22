#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "==> Installing system dependencies..."
sudo apt-get install -y python3-gi python3-gi-cairo gir1.2-gtk-3.0

echo "==> Setting up autostart..."
AUTOSTART_DIR="$HOME/.config/autostart"
mkdir -p "$AUTOSTART_DIR"

DESKTOP_FILE="$AUTOSTART_DIR/todo-ubuntu.desktop"
sed "s|INSTALL_PATH|$SCRIPT_DIR|g" "$SCRIPT_DIR/todo-ubuntu.desktop" > "$DESKTOP_FILE"
chmod 644 "$DESKTOP_FILE"

echo ""
echo "Done! To launch now:"
echo "  python3 $SCRIPT_DIR/todo_app.py"
echo ""
echo "The app will start automatically on your next login."
