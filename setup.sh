#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Setting up the environment..."

# Check if the virtual environment directory exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run the application
echo "Running the application..."
python3 main/main.py

# Run the tests
echo "Running tests..."
python3 -m unittest discover -s tests

# Deactivate the virtual environment
deactivate

echo "Setup, execution, and testing complete."
