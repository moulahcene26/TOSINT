# TOSINT - Project Summary

## Overview
TOSINT is a professional Terminal User Interface (TUI) OSINT Framework built with Python and Textual. It provides a modular, extensible platform for running 33 different OSINT tools across 8 categories.

## Development Timeline

### ✅ Step 1: TUI Skeleton (Complete)
- Created 3-panel layout with Textual
- Implemented navigation (Tab, Shift+Tab, Arrow keys, Enter, Q)
- Professional Flexoki theme
- Responsive design

### ✅ Step 2: Category Selection (Complete)
- Dynamic JSON loading from `data/tools.json`
- Category list population
- Tool list updates based on category
- Click and keyboard navigation support

### ✅ Step 3: Tool Framework (Complete)
- Created `BaseTool` abstract interface
- Implemented `ToolManager` for dynamic tool loading
- Implemented `APIManager` for secure key storage
- API keys stored in `~/Documents/TOSINT/.config/api_keys.json`

### ✅ Step 4: Tool Execution Panel (Complete)
- InputModal for user input
- API key prompting and validation
- Secure key storage with 0600 permissions
- Tool instruction display

### ✅ Step 5: Tool Implementation + CLI Streaming (Complete)
**All 33 tools implemented across 8 categories:**
- Phone Numbers (3 tools)
- Web & URLs (4 tools)
- People & Social Media (4 tools)
- Network & IP Intelligence (4 tools)
- Domains & Infrastructure (6 tools)
- Files & Metadata (3 tools)
- Data Breaches & Leaks (3 tools)
- Misc OSINT (3 tools)

**CLI Streaming Feature:**
- Added RichLog widget for live output
- `supports_streaming()` method in BaseTool
- `run_streaming()` for CLI tools
- Real-time output for Sherlock, Nmap, etc.

### ✅ Step 6: Export & Clipboard (Complete)
- 4 export buttons in UI (Copy, JSON, CSV, MD)
- Clipboard copy with pyperclip
- JSON export with metadata
- CSV export for tabular data
- Markdown formatted reports
- Files saved to `~/Documents/TOSINT/exports/`
- Notification system for export feedback

### ⏳ Step 7: Final Testing & Polish (Ready)
- All core features implemented
- Documentation complete
- Ready for testing

## Technical Architecture

### Core Components
1. **app.py** (749 lines)
   - TOSINTApp class with Textual
   - 3-panel layout (Categories, Tools, Output)
   - InputModal for user input
   - Export button handlers
   - CLI streaming support
   - Flexoki theme

2. **tool_manager.py** (181 lines)
   - Dynamic tool loading from JSON
   - Tool class instantiation
   - Tool statistics

3. **api_manager.py** (89 lines)
   - Secure API key storage
   - Key validation
   - Format checking

### Tool Modules
- **base_tool.py** - Abstract interface
- **phone_tools.py** - 3 phone validation tools
- **web_tools.py** - 4 web analysis tools
- **people_tools.py** - 4 username search tools
- **network_tools.py** - 4 IP/network tools
- **domain_tools.py** - 6 domain enumeration tools
- **file_tools.py** - 3 file metadata tools
- **breach_tools.py** - 3 data breach tools
- **misc_tools.py** - 3 miscellaneous tools

## Working Tools (11+ Fully Functional)

### No API Required
1. ✅ **phonenumbers** - Phone number parsing and validation
2. ✅ **Waybackpy** - Archive.org Wayback Machine queries
3. ✅ **Sherlock** 🖥️ - Username search (requires CLI)
4. ✅ **IPinfo** - IP geolocation and ASN info
5. ✅ **ASN Lookup** - ASN information via BGPView API
6. ✅ **Sublist3r** - Subdomain enumeration
7. ✅ **Nmap** 🖥️ - Port scanning (requires CLI)
8. ✅ **WafW00f** - WAF detection (requires CLI)
9. ✅ **Exiftool** 🖥️ - Metadata extraction (requires CLI)
10. ✅ **pefile** - Windows PE file analysis

### Requires API Key
11. ✅ **HaveIBeenPwned** - Email breach checking

**Legend:**
- ✅ = Fully functional
- 🖥️ = Supports live CLI streaming

## Key Features

### 1. CLI Streaming Output
- Real-time output display for CLI tools
- RichLog widget shows live tool execution
- Progress visibility for long-running operations
- Works with Sherlock, Nmap, Exiftool, etc.

### 2. Secure API Management
- One-time API key entry
- Encrypted storage at `~/Documents/TOSINT/.config/`
- Automatic key reuse
- Format validation

### 3. Export System
- **Clipboard**: Copy results as plain text
- **JSON**: Structured data with metadata
- **CSV**: Tabular format for spreadsheets
- **Markdown**: Formatted reports
- Timestamped filenames
- Organized in exports folder

### 4. Professional UI
- Flexoki theme (warm color palette)
- 3-panel responsive layout
- Color-coded results (green/yellow/red)
- Keyboard and mouse navigation
- Modal dialogs for input
- Notification system

### 5. Modular Architecture
- BaseTool interface for consistency
- Dynamic tool loading from JSON
- Easy to add new tools
- Separation of concerns

## File Structure
```
TOSINT/
├── core/
│   ├── app.py              (749 lines) - Main TUI application
│   ├── tool_manager.py     (181 lines) - Tool loading & management
│   └── api_manager.py      (89 lines)  - API key management
├── tools/
│   ├── base_tool.py        (108 lines) - Abstract tool interface
│   ├── phone_tools.py      (186 lines) - 3 phone tools
│   ├── web_tools.py        (195 lines) - 4 web tools
│   ├── people_tools.py     (242 lines) - 4 people tools
│   ├── network_tools.py    (246 lines) - 4 network tools
│   ├── domain_tools.py     (361 lines) - 6 domain tools
│   ├── file_tools.py       (215 lines) - 3 file tools
│   ├── breach_tools.py     (219 lines) - 3 breach tools
│   └── misc_tools.py       (182 lines) - 3 misc tools
├── data/
│   └── tools.json          - 33 tool definitions
├── main.py                 - Entry point
├── requirements.txt        - Python dependencies
├── install.sh              - Installation script
├── README.md               - User documentation
└── INSTRUCTIONS.md         - Development progress

Total: ~3,000+ lines of Python code
```

## Dependencies
- **textual** (>=0.47.0) - TUI framework
- **tqdm** (>=4.66.0) - Progress bars
- **requests** (>=2.31.0) - HTTP requests
- **phonenumbers** (>=8.13.0) - Phone validation
- **waybackpy** (>=3.0.6) - Archive.org API
- **shodan** (>=1.31.0) - Shodan API
- **sublist3r** (>=1.1) - Subdomain enumeration
- **pefile** (>=2023.2.7) - PE file analysis
- **pyperclip** (>=1.8.2) - Clipboard support

## Installation
```bash
# Quick setup
./install.sh

# Or manual setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Usage Examples

### 1. Phone Number Validation
- Select: Phone Numbers → phonenumbers
- Input: +1-555-123-4567
- Output: Carrier, location, timezone, formats

### 2. Username Search (Streaming)
- Select: People & Social Media → Sherlock
- Input: john_doe
- Watch: Live output as Sherlock searches 400+ sites

### 3. Subdomain Enumeration
- Select: Domains & Infrastructure → Sublist3r
- Input: example.com
- Output: List of discovered subdomains

### 4. IP Geolocation
- Select: Network & IP Intelligence → IPinfo
- Input: 8.8.8.8
- Output: Location, ISP, ASN, timezone

## Future Enhancements
- [ ] Additional tool integrations
- [ ] Dark/Light theme toggle
- [ ] Result history viewer
- [ ] Batch processing mode
- [ ] Plugin system for custom tools
- [ ] Docker containerization
- [ ] Web dashboard interface

## Credits
- **Framework**: Textual by Textualize
- **Theme**: Flexoki by Steph Ango
- **Tools**: Various OSINT community projects

## License
MIT License - Educational and authorized security testing only.

---

**TOSINT** - Professional OSINT in Your Terminal
Version 1.0.0 | Built with Python & Textual
