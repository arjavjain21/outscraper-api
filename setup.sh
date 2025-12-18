#!/bin/bash
# Setup script for Outscraper API

set -e

echo "Setting up Outscraper API..."

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Copy .env.example to .env if .env doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "Please edit .env file with your database credentials"
fi

# Run database migrations
echo "Running database migrations..."
if command -v psql &> /dev/null; then
    echo "Applying performance indexes..."
    sudo -u postgres psql outscraper < migrations/001_add_performance_indexes.sql || echo "Warning: Could not apply migrations. Please run manually."
else
    echo "Warning: psql not found. Please run migrations manually:"
    echo "  sudo -u postgres psql outscraper < migrations/001_add_performance_indexes.sql"
fi

# Run tests
echo "Running tests..."
pytest || echo "Warning: Some tests failed. Please check."

echo ""
echo "Setup complete!"
echo ""
echo "To start the development server:"
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
echo ""
echo "To set up as a systemd service:"
echo "  sudo cp outscraper-api.service /etc/systemd/system/"
echo "  sudo systemctl daemon-reload"
echo "  sudo systemctl enable outscraper-api"
echo "  sudo systemctl start outscraper-api"
