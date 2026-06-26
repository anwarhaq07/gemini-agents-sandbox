#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "🚀 Starting Task Tracker setup..."

# 1. Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed. Please install it and try again."
    exit 1
fi

# 2. Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating Python virtual environment (.venv)..."
    python3 -m venv .venv
else
    echo "✅ Virtual environment already exists."
fi

# 3. Activate virtual environment and install requirements
echo "🔌 Activating virtual environment..."
source .venv/bin/activate

if [ -f "requirements.txt" ]; then
    echo "📥 Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
else
    # Create a default requirements file if missing so pytest works
    echo "📝 Creating default requirements.txt with pytest..."
    echo "pytest" > requirements.txt
    pip install -r requirements.txt
fi

echo "------------------------------------------------"
echo "🎉 Setup complete! Your environment is ready."
echo "------------------------------------------------"
echo "To run your app, use:"
echo "  source .venv/bin/activate"
echo "  python main.py --help"
echo "------------------------------------------------"