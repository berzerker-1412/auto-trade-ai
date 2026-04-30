#!/bin/bash
# Wrapper script for AI translation of wiki/ → wiki_th/
# Calls translate.py with source and destination paths

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/translate.py"

if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "Error: $PYTHON_SCRIPT not found"
    exit 1
fi

exec python3 "$PYTHON_SCRIPT" "$1" "$2"
