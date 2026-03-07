#!/bin/bash
# Test runner script for servo_emulator

echo "Running Servo Emulator Test Suite..."
echo ""

# if venv exists use it otherwise fallback
if [ -d "venv" ]; then
    echo "Using virtual environment."
    ./venv/Scripts/python.exe -m pytest tests/ -v --tb=short
else
    echo "Virtual environment not found, using system python."
    python -m pytest tests/ -v --tb=short
fi

echo ""
echo "Test run complete!"
