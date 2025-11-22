"""
TOSINT - TUI OSINT Framework
Main application using Textual for the interface
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Static, ListView, ListItem, Label, Input, Button
from textual.binding import Binding
from textual.screen import ModalScreen
import json
from pathlib import Path
from core.tool_manager import ToolManager
from core.api_manager import APIManager


class InputModal(ModalScreen):
    """Modal screen for getting user input"""
    
    CSS = """
    InputModal {
        align: center middle;
    }
    
    #input-dialog {
        width: 60;
        height: auto;
        background: $panel;
        border: thick $primary;
        padding: 1 2;
    }
    
    #input-title {
        text-align: center;
        margin-bottom: 1;
    }
    
    #input-field {
        margin: 1 0;
    }
    
    #button-container {
        height: auto;
        align: center middle;
        margin-top: 1;
    }
    
    Button {
        margin: 0 1;
    }
    """
    
    def __init__(self, title: str, prompt: str, is_password: bool = False):
        super().__init__()
        self.title = title
        self.prompt = prompt
        self.is_password = is_password
        self.result = None
        
    def compose(self) -> ComposeResult:
        with Vertical(id="input-dialog"):
            yield Label(self.title, id="input-title")
            yield Label(self.prompt)
            yield Input(placeholder="Enter value...", id="input-field", password=self.is_password)
            with Horizontal(id="button-container"):
                yield Button("Submit", variant="success", id="submit-btn")
                yield Button("Cancel", variant="error", id="cancel-btn")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "submit-btn":
            input_widget = self.query_one("#input-field", Input)
            self.result = input_widget.value
            self.dismiss(self.result)
        else:
            self.dismiss(None)
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle Enter key in input field"""
        self.result = event.value
        self.dismiss(self.result)


class CategoryPanel(Static):
    """Left panel - Category selection"""
    
    def compose(self) -> ComposeResult:
        yield Label("[bold cyan]Categories[/bold cyan]", classes="panel-title")
        yield ListView(id="category-list")


class ToolsPanel(Static):
    """Middle panel - Tools in selected category"""
    
    def compose(self) -> ComposeResult:
        yield Label("[bold yellow]Tools[/bold yellow]", classes="panel-title")
        yield ListView(id="tools-list")


class OutputPanel(Static):
    """Right panel - Tool input/output"""
    
    def compose(self) -> ComposeResult:
        yield Label("[bold green]Input / Output[/bold green]", classes="panel-title")
        yield Static("Select a category and tool to begin", id="output-content", classes="output-content")


class TOSINTApp(App):
    """TOSINT - Terminal OSINT Framework"""
    
    # Use Flexoki theme
    CSS_PATH = None  # We'll define CSS inline
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    Header {
        background: $primary;
        color: $text;
    }
    
    Footer {
        background: $primary;
    }
    
    #main-container {
        height: 100%;
        width: 100%;
    }
    
    CategoryPanel {
        width: 30%;
        height: 100%;
        background: $panel;
        border-right: solid $primary;
        padding: 1;
    }
    
    ToolsPanel {
        width: 30%;
        height: 100%;
        background: $panel;
        border-right: solid $primary;
        padding: 1;
    }
    
    OutputPanel {
        width: 40%;
        height: 100%;
        background: $panel;
        padding: 1;
    }
    
    .panel-title {
        margin-bottom: 1;
        text-align: center;
    }
    
    ListView {
        height: 1fr;
        background: $boost;
        border: solid $primary;
    }
    
    ListView > ListItem {
        padding: 1 2;
    }
    
    ListView > ListItem.--highlight {
        background: $accent;
    }
    
    .output-content {
        height: 1fr;
        background: $boost;
        border: solid $primary;
        padding: 1;
        overflow-y: auto;
    }
    
    .success {
        color: $success;
    }
    
    .warning {
        color: $warning;
    }
    
    .error {
        color: $error;
    }
    """
    
    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),
        Binding("tab", "focus_next", "Next Panel", priority=True),
        Binding("shift+tab", "focus_previous", "Previous Panel", priority=True),
        Binding("enter", "execute_tool", "Execute Tool", priority=True),
    ]
    
    TITLE = "TOSINT - Terminal OSINT Framework"
    SUB_TITLE = "Professional OSINT Tool Suite"
    
    # Set Flexoki theme
    THEME = "flexoki"
    
    def __init__(self):
        super().__init__()
        self.tools_data = {}
        self.selected_category = None
        self.selected_tool = None
        self.tool_manager = ToolManager()
        self.api_manager = APIManager()
        
    def compose(self) -> ComposeResult:
        """Create the main layout"""
        yield Header()
        with Horizontal(id="main-container"):
            yield CategoryPanel(id="category-panel")
            yield ToolsPanel(id="tools-panel")
            yield OutputPanel(id="output-panel")
        yield Footer()
    
    def on_mount(self) -> None:
        """Load tools and populate categories when app starts"""
        self.load_tools()
        self.populate_categories()
        
    def load_tools(self) -> None:
        """Load tools from JSON file using ToolManager"""
        success, message = self.tool_manager.load_tools()
        
        if success:
            self.tools_data = self.tool_manager.tools_data
            self.update_output(f"[green]{message}[/green]")
            
            # Show tool statistics
            stats = self.tool_manager.get_tool_stats()
            stats_msg = f"\n\n[cyan]Statistics:[/cyan]\n"
            stats_msg += f"Categories: {stats['total_categories']}\n"
            stats_msg += f"Total Tools: {stats['total_tools']}\n"
            stats_msg += f"Requires API: {stats['tools_requiring_api']}\n"
            stats_msg += f"No API Required: {stats['tools_without_api']}"
            self.update_output(f"[green]{message}[/green]{stats_msg}")
        else:
            self.update_output(f"[red]Error: {message}[/red]")
            self.tools_data = {}
    
    def populate_categories(self) -> None:
        """Populate the category list"""
        category_list = self.query_one("#category-list", ListView)
        category_list.clear()
        
        for category in self.tools_data.keys():
            label = Label(category)
            item = ListItem(label)
            # Store category name directly on the ListItem
            object.__setattr__(item, 'category_name', category)
            category_list.append(item)
    
    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle list selection events (Enter key)"""
        self._handle_list_selection(event.list_view, event.item)
    
    def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
        """Handle list highlight events (arrow keys/clicks)"""
        # When an item is highlighted, treat it as selected
        self._handle_list_selection(event.list_view, event.item)
    
    def _handle_list_selection(self, list_view: ListView, item: ListItem) -> None:
        """Common handler for list item selection"""
        list_id = list_view.id
        
        if list_id == "category-list":
            # Category selected
            if hasattr(item, 'category_name'):
                self.selected_category = item.category_name
                self.selected_tool = None  # Reset tool selection
                self.populate_tools(self.selected_category)
                self.update_output(f"[cyan]Selected category: {self.selected_category}[/cyan]\n\nSelect a tool from the middle panel")
            
        elif list_id == "tools-list":
            # Tool selected
            if hasattr(item, 'tool_data'):
                self.selected_tool = item.tool_data
                self.show_tool_info(self.selected_tool)
    
    def populate_tools(self, category: str) -> None:
        """Populate tools list for selected category"""
        tools_list = self.query_one("#tools-list", ListView)
        tools_list.clear()
        
        if category in self.tools_data:
            tools = self.tools_data[category]
            for tool in tools:
                label = Label(tool['name'])
                item = ListItem(label)
                # Store tool data directly on the ListItem
                object.__setattr__(item, 'tool_data', tool)
                tools_list.append(item)
    
    def show_tool_info(self, tool: dict) -> None:
        """Display tool information in output panel"""
        info = f"[bold yellow]{tool['name']}[/bold yellow]\n\n"
        info += f"[cyan]Description:[/cyan] {tool['description']}\n\n"
        info += f"[cyan]Integration:[/cyan] {tool['integration']}\n\n"
        
        if tool.get('requires_api'):
            api_link = tool.get('api_link', 'N/A')
            info += f"[yellow]Requires API Key[/yellow]\n"
            info += f"[dim]Get your key at: {api_link}[/dim]\n\n"
        else:
            info += "[green]No API Key Required[/green]\n\n"
        
        info += "[dim]Press Enter to configure and run this tool[/dim]"
        self.update_output(info)
    
    def update_output(self, content: str) -> None:
        """Update the output panel content"""
        output = self.query_one("#output-content", Static)
        output.update(content)
    
    async def action_execute_tool(self) -> None:
        """Handle Enter key to execute selected tool"""
        if self.selected_tool is None:
            self.update_output("[yellow]Please select a tool first[/yellow]")
            return
        
        # Check if tool requires API key
        if self.selected_tool.get('requires_api'):
            tool_name = self.selected_tool.get('name', 'Unknown')
            service_name = tool_name.lower()
            
            # Check if we have the API key
            if not self.api_manager.has_key(service_name):
                api_link = self.selected_tool.get('api_link', 'N/A')
                self.update_output(
                    f"[yellow]API Key Required[/yellow]\n\n"
                    f"This tool requires an API key.\n"
                    f"Get your key at: {api_link}\n\n"
                    f"You will be prompted to enter it..."
                )
                
                # Prompt for API key
                result = await self.push_screen(
                    InputModal(
                        title=f"API Key for {tool_name}",
                        prompt=f"Enter your API key:",
                        is_password=True
                    )
                )
                
                if result:
                    # Validate and save the key
                    is_valid, error_msg = self.api_manager.validate_key_format(service_name, result)
                    if is_valid:
                        self.api_manager.set_key(service_name, result)
                        self.update_output(f"[green]API key saved successfully[/green]")
                    else:
                        self.update_output(f"[red]Invalid API key: {error_msg}[/red]")
                        return
                else:
                    self.update_output("[yellow]API key entry cancelled[/yellow]")
                    return
        
        # Prompt for input data
        tool_name = self.selected_tool.get('name', 'Unknown')
        result = await self.push_screen(
            InputModal(
                title=f"Run {tool_name}",
                prompt="Enter input data (e.g., username, domain, IP):",
                is_password=False
            )
        )
        
        if result:
            # Try to create and run the tool
            tool_instance = self.tool_manager.create_tool_instance(self.selected_tool)
            
            if tool_instance is None:
                self.update_output(
                    f"[yellow]Tool '{tool_name}' not yet implemented[/yellow]\n\n"
                    f"[dim]Input: {result}[/dim]\n\n"
                    f"This tool will be available in a future update."
                )
                return
            
            # Validate input
            is_valid, error_msg = tool_instance.validate_input(result)
            if not is_valid:
                self.update_output(f"[red]Invalid input: {error_msg}[/red]")
                return
            
            # Run the tool
            self.update_output(f"[cyan]Executing {tool_name}...[/cyan]\n\n[dim]Please wait...[/dim]")
            
            # Get API keys if needed
            api_keys = {}
            if self.selected_tool.get('requires_api'):
                service_name = tool_name.lower()
                api_key = self.api_manager.get_key(service_name)
                if api_key:
                    api_keys[service_name] = api_key
            
            # Execute the tool
            try:
                result_data = tool_instance.run(result, api_keys)
                
                # Format and display output
                formatted_output = tool_instance.format_output(result_data)
                
                if result_data.get('success'):
                    self.update_output(
                        f"[bold green]Results for {tool_name}[/bold green]\n\n"
                        f"{formatted_output}\n\n"
                        f"[dim]Execution completed successfully[/dim]"
                    )
                else:
                    self.update_output(
                        f"[bold red]Error executing {tool_name}[/bold red]\n\n"
                        f"{formatted_output}"
                    )
            except Exception as e:
                self.update_output(
                    f"[bold red]Unexpected Error[/bold red]\n\n"
                    f"[red]{str(e)}[/red]"
                )
        else:
            self.update_output("[yellow]Execution cancelled[/yellow]")


def run():
    """Entry point for the application"""
    app = TOSINTApp()
    app.run()


if __name__ == "__main__":
    run()
