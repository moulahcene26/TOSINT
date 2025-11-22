# TOSINT - Terminal OSINT Framework

A professional, modular Python TUI framework for OSINT operations.

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

## Features

- **Multi-panel TUI interface** using Textual
- **8 OSINT categories** with 30+ tools
- **API key management** with secure local storage
- **Export capabilities** (JSON, CSV, Markdown)
- **Color-coded output** for easy reading
- **Progress tracking** with visual indicators

## Navigation

- **Tab / Shift+Tab**: Switch between panels
- **Arrow keys**: Navigate within lists
- **Enter**: Select item / Run tool
- **Q**: Quit application

## Structure

```
TOSINT/
├── core/           # Main application logic
│   └── app.py      # Textual TUI application
├── tools/          # Tool integrations
├── data/           # Configuration and tool definitions
│   └── tools.json  # Tool metadata
├── main.py         # Entry point
└── requirements.txt
```


