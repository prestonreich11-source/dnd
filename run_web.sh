#!/bin/bash
# Start the D&D web game server

echo "=========================================="
echo "  DUNGEONS & ADVENTURES - Web Server"
echo "  Access at http://localhost:5000"
echo "=========================================="
echo ""

# Check if Flask is installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "Installing Flask..."
    pip3 install -r requirements.txt
fi

echo "Starting web server..."
python3 web_app.py
