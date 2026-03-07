@echo off
REM Test runner script for servo_emulator

echo Running Servo Emulator Test Suite...
echo.

REM Check if venv exists
if not exist "venv\" (
    echo Error: Virtual environment not found. Please create it first.
    exit /b 1
)

REM Run tests with pytest
call venv\Scripts\python.exe -m pytest tests/ -v --tb=short

echo.
echo Test run complete!
