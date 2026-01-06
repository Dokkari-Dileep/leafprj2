@echo off
echo Starting AgriDetect Application...
echo.

REM Check if venv exists, if not create it
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install --upgrade pip
pip install flask flask-cors pillow numpy

REM Create necessary directories
if not exist "uploads" mkdir uploads
if not exist "models" mkdir models
if not exist "static" mkdir static

REM Run the application
echo Starting Flask server...
echo Open your browser to: http://localhost:5000
echo.
python app.py

pause