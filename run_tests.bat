@echo off
REM Test runner script for servo_emulator

echo Running Servo Emulator Test Suite...
echo.

REM If venv exists, use it; otherwise fall back to system Python
if exist "venv\" (
    echo "Using virtual environment."
    call venv\Scripts\python.exe -m pytest tests/ -v --tb=short
) else (
    echo "Virtual environment not found, running with system python."
    python -m pytest tests/ -v --tb=short
)

echo.
echo Test run complete!
