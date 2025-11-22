# TOSINT - Terminal OSINT Framework

A professional, modular Python TUI framework for OSINT operations with 33 integrated tools across 8 categories.

## Features

🎯 **Multi-panel TUI interface** using Textual with Flexoki theme
📊 **8 OSINT categories** with 33 integrated tools
🔐 **Secure API key management** stored in `~/Documents/TOSINT/.config/`
📤 **Export capabilities** (JSON, CSV, Markdown, Clipboard)
🖥️ **CLI tool streaming** - Live output for tools like Sherlock and Nmap
🎨 **Color-coded output** for easy reading
⚡ **Progress tracking** with visual indicators

## Installation

### 1. Create Virtual Environment (Recommended)

```bash
cd TOSINT
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate  # On Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Optional CLI Tools

Some tools require external CLI applications:

```bash
# Username search tools
pip install sherlock-project

# Network tools
sudo apt install nmap  # Linux
brew install nmap      # macOS

# Metadata extraction
sudo apt install exiftool  # Linux
brew install exiftool      # macOS

# WAF detection
pip install wafw00f
```

### 4. Run TOSINT

```bash
python main.py
```

## Tool Categories

### 📞 Phone Numbers (3 tools)
- **phonenumbers** ✅ - Phone validation and carrier lookup
- **Numverify** - Phone API validation (requires API key)
- **Truecaller Unofficial** - Caller ID lookup

### 🌐 Web & URLs (4 tools)
- **Waybackpy** ✅ - Archive.org Wayback Machine queries
- **WhatWeb** - Web technology identification
- **Aquatone** - Screenshot & subdomain takeover
- **Photon** - Web crawler & data extractor

### 👥 People & Social Media (4 tools)
- **Sherlock** ✅🖥️ - Username search across 400+ sites
- **Maigret** - Enhanced username search
- **Snoop** - Russian social networks search
- **EmailHarvester** - Email scraping from domains

### 🌍 Network & IP Intelligence (4 tools)
- **Shodan** - IoT/device search (requires API key)
- **Censys** - Internet-wide scanning (requires API key)
- **IPinfo** ✅ - IP geolocation & ASN info
- **ASN Lookup** ✅ - BGP/ASN information

### 🔍 Domains & Infrastructure (6 tools)
- **theHarvester** - Email & subdomain harvesting
- **Sublist3r** ✅ - Subdomain enumeration
- **Amass** - Attack surface mapping
- **DNSRecon** - DNS enumeration
- **Nmap** ✅🖥️ - Port scanning & network discovery
- **WafW00f** ✅ - WAF detection

### 📁 Files & Metadata (3 tools)
- **Exiftool** ✅🖥️ - Metadata extraction from images/documents
- **pefile** ✅ - Windows PE file analysis
- **Yara** - Pattern-based file scanning

### 🔓 Data Breaches & Leaks (3 tools)
- **HaveIBeenPwned** ✅ - Email breach checking (requires API key)
- **Dehashed** - Leaked credentials search (requires API key)
- **BreachDirectory** - Local breach database search

### 🔧 Misc OSINT (3 tools)
- **GHunt** - Google account investigation
- **Creepy** - Geolocation OSINT
- **SpiderFoot** - Automated OSINT collection

**Legend:**
- ✅ = Fully functional and tested
- 🖥️ = Supports live CLI streaming output
- 🔑 = Requires API key

## Navigation

| Key | Action |
|-----|--------|
| **Tab / Shift+Tab** | Switch between panels |
| **Arrow keys** | Navigate within lists |
| **Enter** | Select item / Run tool |
| **Q** | Quit application |

## Export Options

After running a tool, use the export buttons:
- **📋 Copy** - Copy results to clipboard
- **JSON** - Export as JSON with metadata
- **CSV** - Export as CSV table
- **MD** - Export as Markdown report

All exports saved to: `~/Documents/TOSINT/exports/`

## API Key Management

1. Run a tool that requires an API key
2. You'll be prompted to enter it once
3. Keys are securely stored in `~/Documents/TOSINT/.config/api_keys.json`
4. Keys are reused automatically on future runs

**Get API Keys:**
- HaveIBeenPwned: https://haveibeenpwned.com/API/Key
- Shodan: https://account.shodan.io/
- Censys: https://search.censys.io/account/api
- Numverify: https://numverify.com/
- Dehashed: https://dehashed.com/

## Project Structure

```
TOSINT/
├── core/
│   ├── app.py           # Main Textual application
│   ├── tool_manager.py  # Tool loading & execution
│   └── api_manager.py   # Secure API key management
├── tools/
│   ├── base_tool.py     # Base tool interface
│   ├── phone_tools.py   # Phone number tools
│   ├── web_tools.py     # Web & URL tools
│   ├── people_tools.py  # Username & social media tools
│   ├── network_tools.py # Network & IP tools
│   ├── domain_tools.py  # Domain enumeration tools
│   ├── file_tools.py    # File metadata tools
│   ├── breach_tools.py  # Data breach tools
│   └── misc_tools.py    # Miscellaneous OSINT tools
├── data/
│   └── tools.json       # Tool metadata
├── main.py              # Entry point
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## Requirements

- Python 3.10+
- See `requirements.txt` for Python packages
- Optional: CLI tools (nmap, sherlock, exiftool, etc.)

## Development

TOSINT follows a modular architecture:
1. **BaseTool** interface in `tools/base_tool.py`
2. Each tool implements: `validate_input()`, `run()`, `format_output()`
3. CLI tools can enable `supports_streaming()` for live output
4. Tools are auto-loaded from `data/tools.json`

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Follow the BaseTool interface pattern
4. Submit a pull request

## Disclaimer

This tool is for educational and authorized security testing only. Users are responsible for complying with all applicable laws and regulations. Unauthorized access to computer systems is illegal.


