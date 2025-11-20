#!/bin/bash

# JDMI Assessment Tool - Quick Start Script

echo "🚀 Starting JDMI Assessment Tool..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Check if required packages are installed
echo ""
echo "📦 Checking dependencies..."

if ! python3 -c "import streamlit" &> /dev/null; then
    echo "⚠️  Streamlit not found. Installing dependencies..."
    pip3 install -r requirements.txt
else
    echo "✅ Dependencies installed"
fi

# Run the Streamlit app
echo ""
echo "🌐 Launching JDMI Assessment Tool..."
echo "   → Access at: http://localhost:8501"
echo "   → Press Ctrl+C to stop"
echo ""

streamlit run app.py

