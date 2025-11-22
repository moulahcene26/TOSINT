"""
Tool Manager - Load and execute OSINT tools dynamically
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from tools.base_tool import BaseTool

# Import tool implementations
from tools.phone_tools import PhoneNumbersTool, NumverifyTool, TruecallerTool
from tools.web_tools import WaybackpyTool, WhatWebTool, AquatoneTool, PhotonTool
from tools.people_tools import SherlockTool, MaigretTool, SnoopTool, EmailHarvesterTool
from tools.network_tools import ShodanTool, CensysTool, IPinfoTool, ASNLookupTool
from tools.domain_tools import (TheHarvesterTool, Sublist3rTool, AmassTool, 
                                DNSReconTool, NmapTool, WafW00fTool)
from tools.file_tools import ExiftoolTool, PefileTool, YaraTool
from tools.breach_tools import HaveIBeenPwnedTool, DehashedTool, BreachDirectoryTool
from tools.misc_tools import GHuntTool, CreepyTool, SpiderFootTool


class ToolManager:
    """Manage loading and execution of OSINT tools"""
    
    def __init__(self, tools_json_path: Optional[Path] = None):
        """
        Initialize tool manager
        
        Args:
            tools_json_path: Path to tools.json file
        """
        if tools_json_path is None:
            tools_json_path = Path(__file__).parent.parent / "data" / "tools.json"
        
        self.tools_json_path = tools_json_path
        self.tools_data: Dict[str, List[dict]] = {}
        self.tool_instances: Dict[str, BaseTool] = {}
        
    def load_tools(self) -> tuple[bool, str]:
        """
        Load tools from JSON file
        
        Returns:
            Tuple of (success, message)
        """
        try:
            with open(self.tools_json_path, 'r') as f:
                self.tools_data = json.load(f)
            
            count = sum(len(tools) for tools in self.tools_data.values())
            return True, f"Loaded {len(self.tools_data)} categories with {count} tools"
        except FileNotFoundError:
            return False, "tools.json not found"
        except json.JSONDecodeError as e:
            return False, f"Error parsing tools.json: {e}"
        except Exception as e:
            return False, f"Unexpected error loading tools: {e}"
    
    def get_categories(self) -> List[str]:
        """
        Get list of all tool categories
        
        Returns:
            List of category names
        """
        return list(self.tools_data.keys())
    
    def get_tools_in_category(self, category: str) -> List[dict]:
        """
        Get all tools in a specific category
        
        Args:
            category: Category name
            
        Returns:
            List of tool dictionaries
        """
        return self.tools_data.get(category, [])
    
    def get_tool_by_name(self, tool_name: str) -> Optional[dict]:
        """
        Find a tool by name across all categories
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            Tool dictionary or None if not found
        """
        for category, tools in self.tools_data.items():
            for tool in tools:
                if tool.get('name') == tool_name:
                    return tool
        return None
    
    def create_tool_instance(self, tool_data: dict) -> Optional[BaseTool]:
        """
        Create a tool instance based on tool name
        
        Args:
            tool_data: Tool metadata dictionary
            
        Returns:
            BaseTool instance or None
        """
        tool_name = tool_data.get('name')
        
        # Check if we already have an instance
        if tool_name in self.tool_instances:
            return self.tool_instances[tool_name]
        
        # Map tool names to their implementation classes
        tool_map = {
            # Phone Numbers
            'phonenumbers': PhoneNumbersTool,
            'Numverify': NumverifyTool,
            'Truecaller Unofficial': TruecallerTool,
            
            # Web & URLs
            'Waybackpy': WaybackpyTool,
            'WhatWeb': WhatWebTool,
            'Aquatone': AquatoneTool,
            'Photon': PhotonTool,
            
            # People & Social Media
            'Sherlock': SherlockTool,
            'Maigret': MaigretTool,
            'Snoop': SnoopTool,
            'EmailHarvester': EmailHarvesterTool,
            
            # Network & IP Intelligence
            'Shodan': ShodanTool,
            'Censys': CensysTool,
            'IPinfo': IPinfoTool,
            'ASN Lookup': ASNLookupTool,
            
            # Domains & Infrastructure
            'theHarvester': TheHarvesterTool,
            'Sublist3r': Sublist3rTool,
            'Amass': AmassTool,
            'DNSRecon': DNSReconTool,
            'Nmap': NmapTool,
            'WafW00f': WafW00fTool,
            
            # Files & Metadata
            'Exiftool': ExiftoolTool,
            'pefile': PefileTool,
            'Yara': YaraTool,
            
            # Data Breaches & Leaks
            'HaveIBeenPwned': HaveIBeenPwnedTool,
            'Dehashed': DehashedTool,
            'BreachDirectory': BreachDirectoryTool,
            
            # Misc OSINT
            'GHunt': GHuntTool,
            'Creepy': CreepyTool,
            'SpiderFoot': SpiderFootTool,
        }
        
        tool_class = tool_map.get(tool_name)
        if tool_class:
            instance = tool_class(tool_data)
            self.tool_instances[tool_name] = instance
            return instance
        
        # Tool not yet implemented
        return None
    
    def get_tool_stats(self) -> Dict[str, Any]:
        """
        Get statistics about loaded tools
        
        Returns:
            Dictionary with tool statistics
        """
        total_tools = sum(len(tools) for tools in self.tools_data.values())
        tools_requiring_api = 0
        
        for tools in self.tools_data.values():
            for tool in tools:
                if tool.get('requires_api', False):
                    tools_requiring_api += 1
        
        return {
            'total_categories': len(self.tools_data),
            'total_tools': total_tools,
            'tools_requiring_api': tools_requiring_api,
            'tools_without_api': total_tools - tools_requiring_api
        }
