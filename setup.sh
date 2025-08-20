#!/bin/bash

echo "========================================"
echo "  Distributed Database System Setup"
echo "========================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

echo "Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "Error: Failed to create virtual environment"
    echo "Please ensure Python 3 is installed and in PATH"
    exit 1
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi

echo "Creating migrations..."
python manage.py makemigrations data_simulation
if [ $? -ne 0 ]; then
    echo "Error: Failed to create migrations"
    exit 1
fi

echo "Applying migrations..."
python manage.py migrate
if [ $? -ne 0 ]; then
    echo "Error: Failed to apply migrations"
    exit 1
fi

echo
echo "========================================"
echo "  Setup Complete! 🎉"
echo "========================================"
echo
echo "You can now run:"
echo "  python manage.py generate_pdf_report"
echo
echo "Or for basic simulation:"
echo "  python manage.py simulate_insertions"
echo
echo "To activate the virtual environment later:"
echo "  source venv/bin/activate"
echo
