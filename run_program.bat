@echo off
echo Starting Brew Empire Business Manager...
python coffee_manager.py
if %ERRORLEVEL% == 0 (
    echo Program ran successfully.
) else (
    echo Failed to run program. Please ensure Python is installed and coffee_manager.py is in this directory.
)
pause