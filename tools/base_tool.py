"""
BaseTool - Interface for all OSINT tools in TOSINT
Every tool must implement this interface
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseTool(ABC):
    """Base class for all OSINT tools"""
    
    def __init__(self, tool_data: dict):
        """
        Initialize tool with metadata from JSON
        
        Args:
            tool_data: Dictionary containing tool metadata
        """
        self.name = tool_data.get('name', 'Unknown Tool')
        self.description = tool_data.get('description', 'No description available')
        self.integration = tool_data.get('integration', 'unknown')
        self.requires_api = tool_data.get('requires_api', False)
        self.api_link = tool_data.get('api_link', None)
        
    @abstractmethod
    def validate_input(self, input_data: str) -> tuple[bool, str]:
        """
        Validate input data before execution
        
        Args:
            input_data: User input string
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        pass
    
    @abstractmethod
    def run(self, input_data: str, api_keys: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Execute the tool with provided input
        
        Args:
            input_data: User input (username, domain, IP, etc.)
            api_keys: Dictionary of API keys if required
            
        Returns:
            Dictionary with results:
            {
                'success': bool,
                'data': Any,
                'error': str (if success=False)
            }
        """
        pass
    
    def get_input_prompt(self) -> str:
        """
        Get the input prompt message for this tool
        
        Returns:
            String prompt to display to user
        """
        return f"Enter input for {self.name}:"
    
    def format_output(self, result: Dict[str, Any]) -> str:
        """
        Format the result for display in TUI
        
        Args:
            result: Result dictionary from run()
            
        Returns:
            Formatted string for display
        """
        if not result.get('success'):
            return f"[red]Error: {result.get('error', 'Unknown error')}[/red]"
        
        data = result.get('data', {})
        if isinstance(data, dict):
            output = []
            for key, value in data.items():
                output.append(f"[cyan]{key}:[/cyan] {value}")
            return "\n".join(output)
        elif isinstance(data, list):
            return "\n".join([f"- {item}" for item in data])
        else:
            return str(data)
