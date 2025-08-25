#!/bin/bash
echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║           🚀 SKYLUS ANALYTICS PLATFORM                      ║"
echo "║              Starting Enterprise Dashboard...               ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "🌐 Starting server on http://localhost:9501"
echo "📊 Loading professional interface..."
echo "⚡ Initializing analytics engine..."
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "🔧 Activating virtual environment..."
    source venv/bin/activate
fi

# Start Skylus Analytics Platform
python -m streamlit run main.py --server.port 9501 --server.headless true

echo ""
echo "👋 Skylus Analytics Platform stopped."
