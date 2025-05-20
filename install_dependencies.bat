@echo off
echo Installing dependencies for Brew Empire Business Manager...
pip install -r requirements.txt
if %ERRORLEVEL% == 0 (
    echo Dependencies installed successfully.
) else (
    echo Failed to install dependencies. Please ensure pip is installed and try: pip install -r requirements.txt
)
pause