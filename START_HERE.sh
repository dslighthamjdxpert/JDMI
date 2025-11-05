#!/bin/bash
# JDMI Assessment - Quick Start Script

echo "🚀 JDMI Assessment Tool - Quick Start"
echo "======================================"
echo ""

# Navigate to correct directory
cd "$(dirname "$0")"

echo "📂 Current directory: $(pwd)"
echo ""

# Check Python
echo "✓ Python found: $(python3 --version)"
echo ""

# Check if streamlit is installed
echo "📦 Checking dependencies..."
if python3 -c "import streamlit" 2>/dev/null; then
    echo "✓ Streamlit already installed"
else
    echo "⚙️  Installing dependencies (this may take 1-2 minutes)..."
    pip3 install -q streamlit plotly pandas numpy
    echo "✓ Installation complete!"
fi

echo ""
echo "🌐 Starting JDMI Assessment Tool..."
echo ""
echo "→ The app will open in your browser at: http://localhost:8501"
echo "→ Press Ctrl+C to stop the app"
echo ""
echo "======================================"
echo ""

# Run the app
python3 -m streamlit run app.py

