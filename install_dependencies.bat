@echo off
echo Welcome to Brew Empire Business Manager Dependency Installer
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python is not installed or not found in PATH. Please install Python 3.8 or higher.
    echo Download Python from: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Inform user about the process
echo This script will:
echo 1. Create a virtual environment (venv) to isolate dependencies.
echo 2. Install required packages: pandas, openpyxl, dash, plotly, dash-bootstrap-components, flask.
echo This ensures no changes to your system’s Python setup.
echo Press Ctrl+C to cancel or any key to continue...
pause >nul

:: Create virtual environment
echo Creating virtual environment in 'venv' folder...
python -m venv venv
if %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to create virtual environment. Please ensure the 'venv' module is available.
    pause
    exit /b 1
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to activate virtual environment.
    pause
    exit /b 1
)

:: Install dependencies
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt
if %ERRORLEVEL% == 0 (
    echo Dependencies installed successfully in the virtual environment.
    echo.
    echo To run the program:
    echo 1. Double-click 'run_program.bat' in the project folder.
    echo 2. Or, open a command prompt, activate the environment with 'call venv\Scripts\activate.bat', then run 'python your_script_name.py'.
    echo.
    echo To uninstall, simply delete the project folder (including 'venv').
) else (
    echo Error: Failed to install dependencies.
    echo Try running 'pip install -r requirements.txt' manually after activating the virtual environment.
    echo To activate: call venv\Scripts\activate.bat
)
pause