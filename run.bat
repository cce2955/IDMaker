@echo off

REM Check if .venv exists
if not exist .venv\ (
    echo Creating virtual environment...
    python -m venv .venv
    echo Virtual environment created.
)

REM Activate the virtual environment
call .venv\Scripts\activate.bat

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt
echo Requirements installed.

REM Run the Python script in a loop
python download_libraries.py


REM Deactivate the virtual environment
deactivate
