"""
Miscellaneous OSINT Tools
Implements various other useful OSINT tools
"""

from tools.base_tool import BaseTool
from typing import Dict, Any, Optional
import subprocess
import shutil
import re


class GHuntTool(BaseTool):
    """Google account investigation using GHunt"""
    
    def validate_input(self, input_data: str) -> tuple[bool, str]:
        """Validate email address"""
        if not input_data or not input_data.strip():
            return False, "Email address cannot be empty"
        
        email = input_data.strip()
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return False, "Invalid email address format"
        
        return True, ""
    
    def run(self, input_data: str, api_keys: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Investigate Google account using GHunt tool
        
        Requires GHunt installation: pip install ghunt
        Documentation: https://github.com/mxrch/GHunt
        """
        email = input_data.strip()
        
        if not shutil.which('ghunt'):
            return {
                'success': False,
                'error': 'GHunt is not installed. Install with: pip install ghunt\n' \
                        'Then run: ghunt login (one-time setup)'
            }
        
        try:
            # Run GHunt
            result = subprocess.run(
                ['ghunt', 'email', email],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if 'not logged in' in result.stderr.lower() or 'not logged in' in result.stdout.lower():
                return {
                    'success': False,
                    'error': 'GHunt not configured. Run: ghunt login (one-time setup)'
                }
            
            if result.returncode != 0:
                return {
                    'success': False,
                    'error': f'GHunt failed: {result.stderr}'
                }
            
            # Parse output
            output = result.stdout
            
            result_data = {
                'Email': email,
                'Output': output[:2000]  # Limit output
            }
            
            return {
                'success': True,
                'data': result_data
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'GHunt timed out after 30 seconds'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'GHunt error: {str(e)}'
            }


class CreepyTool(BaseTool):
    """Geolocation OSINT tool"""
    
    def validate_input(self, input_data: str) -> tuple[bool, str]:
        """Validate username or input"""
        if not input_data or not input_data.strip():
            return False, "Input cannot be empty"
        return True, ""
    
    def run(self, input_data: str, api_keys: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Gather geolocation information using Creepy
        
        This tool is GUI-based and not suitable for TUI integration
        """
        return {
            'success': False,
            'error': 'Creepy is a GUI tool not suitable for TUI integration.\n' \
                    'Download: https://www.geocreepy.com/'
        }


class SpiderFootTool(BaseTool):
    """Automated OSINT collection using SpiderFoot"""
    
    def validate_input(self, input_data: str) -> tuple[bool, str]:
        """Validate target (domain, IP, email, etc.)"""
        if not input_data or not input_data.strip():
            return False, "Target cannot be empty"
        return True, ""
    
    def run(self, input_data: str, api_keys: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Run SpiderFoot scan
        
        SpiderFoot is a powerful OSINT automation tool but requires
        installation and typically runs as a web server
        """
        target = input_data.strip()
        
        # Check if SpiderFoot CLI is available
        if not shutil.which('spiderfoot'):
            return {
                'success': False,
                'error': 'SpiderFoot not installed.\n' \
                        'Install: pip install spiderfoot\n' \
                        'Or download: https://github.com/smicallef/spiderfoot\n\n' \
                        'Note: SpiderFoot works best as a web interface (spiderfoot -l 127.0.0.1:5001)'
            }
        
        try:
            # Run basic SpiderFoot scan
            result = subprocess.run(
                ['spiderfoot', '-s', target, '-t', 'IP_ADDRESS,DOMAIN_NAME', '-q'],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                return {
                    'success': False,
                    'error': f'SpiderFoot failed: {result.stderr}'
                }
            
            output = result.stdout
            
            result_data = {
                'Target': target,
                'Output': output[:2000]  # Limit output
            }
            
            return {
                'success': True,
                'data': result_data
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'SpiderFoot timed out after 60 seconds'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'SpiderFoot error: {str(e)}'
            }
