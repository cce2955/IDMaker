@echo off
REM Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python and try again.
    exit /b 1
)

REM Ask the user for a URL
set /p url="Please enter a URL: "

REM Create a virtual environment folder named .venv
python -m venv .venv

REM Activate the virtual environment
call .venv\Scripts\activate

REM Install required libraries from requirements.txt
pip install -r requirements.txt

REM Run the Python script and pass the URL as an argument
python download_libraries.py "%url%"

REM Deactivate the virtual environment
deactivate
