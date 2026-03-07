#!/bin/bash
# Test runner script for servo_emulator

echo "Running Servo Emulator Test Suite..."
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found. Please create it first."
    exit 1
fi

# Run tests with pytest
./venv/Scripts/python.exe -m pytest tests/ -v --tb=short

echo ""
echo "Test run complete!"
