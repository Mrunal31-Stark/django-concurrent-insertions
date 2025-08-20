@echo off
echo ========================================
echo   Distributed Database System Setup
echo ========================================
echo.

echo Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo Error: Failed to create virtual environment
    echo Please ensure Python is installed and in PATH
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo Creating migrations...
python manage.py makemigrations data_simulation
if %errorlevel% neq 0 (
    echo Error: Failed to create migrations
    pause
    exit /b 1
)

echo Applying migrations...
python manage.py migrate
if %errorlevel% neq 0 (
    echo Error: Failed to apply migrations
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Setup Complete! 🎉
echo ========================================
echo.
echo You can now run:
echo   python manage.py generate_pdf_report
echo.
echo Or for basic simulation:
echo   python manage.py simulate_insertions
echo.
pause
