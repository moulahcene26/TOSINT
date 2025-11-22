#!/bin/bash
# TOSINT Installation Script

echo "================================"
echo "  TOSINT Framework Installer"
echo "================================"
echo ""

# Check Python version
echo "[1/5] Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.10 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ Found Python $PYTHON_VERSION"

# Create virtual environment
echo ""
echo "[2/5] Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "[3/5] Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

# Install Python dependencies
echo ""
echo "[4/5] Installing Python dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt
echo "✓ Python dependencies installed"

# Create config directory
echo ""
echo "[5/5] Creating configuration directory..."
mkdir -p ~/Documents/TOSINT/.config
mkdir -p ~/Documents/TOSINT/exports
chmod 700 ~/Documents/TOSINT/.config
echo "✓ Configuration directory created at ~/Documents/TOSINT/"

echo ""
echo "================================"
echo "  Installation Complete! ✓"
echo "================================"
echo ""
echo "To run TOSINT:"
echo "  1. source venv/bin/activate"
echo "  2. python main.py"
echo ""
echo "Optional CLI tools (install separately):"
echo "  • Sherlock:  pip install sherlock-project"
echo "  • Nmap:      sudo apt install nmap (Linux) / brew install nmap (macOS)"
echo "  • Exiftool:  sudo apt install exiftool (Linux) / brew install exiftool (macOS)"
echo "  • WafW00f:   pip install wafw00f"
echo ""
echo "Get API keys at:"
echo "  • HaveIBeenPwned: https://haveibeenpwned.com/API/Key"
echo "  • Shodan:         https://account.shodan.io/"
echo "  • Censys:         https://search.censys.io/account/api"
echo ""
