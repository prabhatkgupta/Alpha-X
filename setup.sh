#!/bin/bash

# Setup script for Alpha-X

echo "=================================="
echo "Alpha-X - Setup"
echo "=================================="
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "=================================="
echo "✅ Setup complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Create .env file (copy from .env.example)"
echo "2. Add your Google Sheets credentials to credentials/"
echo "3. Configure your Twilio credentials in .env"
echo "4. Run: python src/test_connection.py"
echo ""
echo "To activate the virtual environment:"
echo "  source venv/bin/activate"
echo ""

