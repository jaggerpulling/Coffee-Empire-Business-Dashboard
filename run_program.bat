@echo off
echo Starting Brew Empire Business Manager...
echo.

:: Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Error: Virtual environment not found. Please run 'install_dependencies.bat' first.
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

:: Run the program
echo Launching the program...
coffee_manager.py
if %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to run the program. Ensure 'main.py' exists and is compatible with the installed dependencies.
    echo You can also try running manually: python main.py
)

pause