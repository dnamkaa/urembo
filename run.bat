@echo off
REM Smart Retail System - Windows Startup Script
REM Tanzania POS & Inventory Management

cls
echo ========================================================
echo Smart Retail System - Products Module
echo Tanzania POS ^& Inventory Management
echo ========================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found. Please install Python 3.8+
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Create virtual environment if not exists
if not exist ".venv" (
    echo [1/4] Creating virtual environment...
    python -m venv .venv
    echo Virtual environment created
) else (
    echo [1/4] Virtual environment already exists
)

REM Activate virtual environment
echo [2/4] Installing dependencies...
call .venv\Scripts\activate.bat
pip install -r requirements.txt >nul 2>&1

if errorlevel 1 (
    echo Warning: Some dependencies may not have installed properly
) else (
    echo Dependencies installed
)

REM Initialize database
echo [3/4] Initializing database...
python -c "from app import app, init_db, seed_sample_data; import sys; sys.path.insert(0, '.'); app.app_context().push(); init_db(); seed_sample_data()" >nul 2>&1
echo Database initialized

REM Run the application
echo.
echo [4/4] Starting Smart Retail System...
echo ========================================================
echo Smart Retail System is running!
echo.
echo Open your browser: http://127.0.0.1:5000
echo.
echo Press CTRL+C to stop the server
echo.
echo API Endpoints:
echo   GET    http://127.0.0.1:5000/api/v1/products
echo   GET    http://127.0.0.1:5000/api/v1/products/stats
echo   GET    http://127.0.0.1:5000/api/v1/categories
echo   POST   http://127.0.0.1:5000/api/v1/products
echo ========================================================
echo.

python app.py

pause
