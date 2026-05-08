#!/bin/bash

echo "🌤️  My Dark Sky - Setup Script"
echo "================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+"
    exit 1
fi

echo "✓ Python found: $(python3 --version)"

# Check if .env exists
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your OPENWEATHER_API_KEY"
    echo ""
    echo "Get your free API key from: https://openweathermap.org/api"
    echo ""
fi

# Install dependencies
echo ""
echo "Installing dependencies..."
pip3 install -r requirements.txt --break-system-packages 2>/dev/null || pip3 install -r requirements.txt

echo ""
echo "✓ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your OpenWeather API key"
echo "2. Run: python3 app.py"
echo "3. Open: http://localhost:5000"
echo ""
echo "For deployment instructions, see DEPLOYMENT.md"
echo ""
