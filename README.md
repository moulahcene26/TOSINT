# TOSINT - Terminal OSINT Framework

Python TUI OSINT framework with 33 tools across 8 categories.

## Features

- Interactive shell interface with Flexoki theme
- 33 integrated OSINT tools
- Secure API key storage
- Export to JSON/CSV/MD/Clipboard
- Live CLI streaming
- Color-coded output

## Installation

### 1. Create Virtual Environment

```bash
cd TOSINT
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Optional CLI Tools

```bash
pip install sherlock-project wafw00f
sudo apt install nmap exiftool  # Linux
brew install nmap exiftool      # macOS
```

### 4. Run TOSINT

```bash
python main.py
```

## Tool Categories

### Phone Numbers (3 tools)
- phonenumbers - Phone validation and carrier lookup
- Numverify - Phone API validation (requires API key)
- Truecaller Unofficial - Caller ID lookup

### Web & URLs (4 tools)
- Waybackpy - Archive.org Wayback Machine queries
- WhatWeb - Web technology identification
- Aquatone - Screenshot & subdomain takeover
- Photon - Web crawler & data extractor

### People & Social Media (4 tools)
- Sherlock - Username search across 400+ sites (CLI streaming)
- Maigret - Enhanced username search
- Snoop - Russian social networks search
- EmailHarvester - Email scraping from domains

### Network & IP Intelligence (4 tools)
- Shodan - IoT/device search (requires API key)
- Censys - Internet-wide scanning (requires API key)
- IPinfo - IP geolocation & ASN info
- ASN Lookup - BGP/ASN information

### Domains & Infrastructure (6 tools)
- theHarvester - Email & subdomain harvesting
- Sublist3r - Subdomain enumeration
- Amass - Attack surface mapping
- DNSRecon - DNS enumeration
- Nmap - Port scanning & network discovery (CLI streaming)
- WafW00f - WAF detection

### Files & Metadata (3 tools)
- Exiftool - Metadata extraction from images/documents (CLI streaming)
- pefile - Windows PE file analysis
- Yara - Pattern-based file scanning

### Data Breaches & Leaks (3 tools)
- HaveIBeenPwned - Email breach checking (requires API key)
- Dehashed - Leaked credentials search (requires API key)
- BreachDirectory - Local breach database search

### Misc OSINT (3 tools)
- GHunt - Google account investigation
- Creepy - Geolocation OSINT
- SpiderFoot - Automated OSINT collection

## Navigation

| Key | Action |
|-----|--------|
| Tab / Shift+Tab | Switch between panels |
| Arrow keys | Navigate within lists |
| Enter | Select item / Run tool |
| Q | Quit application |

## Shell Commands

When a tool is open:
- Type your input and press Enter
- `help` - Show available commands
- `clear` - Clear shell output
- `exit` or `quit` - Close current tool

## Export Options

After running a tool:
- Copy - Copy results to clipboard
- JSON - Export as JSON with metadata
- CSV - Export as CSV table
- MD - Export as Markdown report

Exports saved to: `~/Documents/TOSINT/exports/`

## API Keys

API keys are stored securely in `~/Documents/TOSINT/.config/api_keys.json`

Get keys at:
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
- Python packages in `requirements.txt`
- Optional: CLI tools (nmap, sherlock, exiftool)

## Development

Modular architecture with `BaseTool` interface:
- Each tool implements: `validate_input()`, `run()`, `format_output()`
- CLI streaming support via `supports_streaming()`
- Tools auto-loaded from `data/tools.json`

## License

MIT License

## Contributing

Fork, create feature branch, follow BaseTool pattern, submit PR.

## Disclaimer

For educational and authorized testing only. Users responsible for legal compliance.


