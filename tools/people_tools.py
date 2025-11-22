"""
People & Social Media OSINT Tools
Implements tools for username enumeration and social media investigation
"""

from tools.base_tool import BaseTool
from typing import Dict, Any, Optional
import subprocess
import json
import shutil


class SherlockTool(BaseTool):
    """Find usernames across social networks using Sherlock"""
    
    def supports_streaming(self) -> bool:
        """Sherlock supports streaming output"""
        return True
    
    def validate_input(self, input_data: str) -> tuple[bool, str]:
        """Validate username input"""
        if not input_data or not input_data.strip():
            return False, "Username cannot be empty"
        
        username = input_data.strip()
        if len(username) < 2:
            return False, "Username must be at least 2 characters"
        
        if ' ' in username:
            return False, "Username cannot contain spaces"
        
        return True, ""
    
    def run_streaming(self, input_data: str, api_keys: Optional[Dict[str, str]] = None):
        """
        Run Sherlock with streaming output
        
        Returns:
            subprocess.Popen object
        """
        username = input_data.strip()
        
        # Check if sherlock is installed
        if not shutil.which('sherlock'):
            raise RuntimeError('Sherlock is not installed. Install it with: pip install sherlock-project')
        
        # Start sherlock process with streaming output
        process = subprocess.Popen(
            ['sherlock', username, '--timeout', '10'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1,
            universal_newlines=False
        )
        
        return process

    
    def run(self, input_data: str, api_keys: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Search for username across social networks using Sherlock CLI
        
        Args:
            input_data: Username to search for
            api_keys: Not used for this tool
            
        Returns:
            Dictionary with found profiles
        """
        username = input_data.strip()
        
        # Check if sherlock is installed
        if not shutil.which('sherlock'):
            return {
                'success': False,
                'error': 'Sherlock is not installed. Install it with: pip install sherlock-project'
            }
        
        try:
            # Run sherlock command
            result = subprocess.run(
                ['sherlock', username, '--timeout', '10', '--print-found'],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0 and not result.stdout:
                return {
                    'success': False,
                    'error': f'Sherlock command failed: {result.stderr}'
                }
            
            # Parse output
            lines = result.stdout.strip().split('\n')
            found_profiles = []
            
            for line in lines:
                if line.strip() and not line.startswith('['):
                    # Clean up the line
                    cleaned = line.strip()
                    if 'http' in cleaned:
                        found_profiles.append(cleaned)
            
            if not found_profiles:
                return {
                    'success': True,
                    'data': {
                        'Username': username,
                        'Status': 'No profiles found',
                        'Note': 'This username may not exist on popular social networks'
                    }
                }
            
            return {
                'success': True,
                'data': {
                    'Username': username,
                    'Profiles Found': len(found_profiles),
                    'Results': '\n' + '\n'.join([f'  • {url}' for url in found_profiles])
                }
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Sherlock search timed out after 60 seconds'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Error running Sherlock: {str(e)}'
            }


class MaigretTool(BaseTool):
    """Advanced username enumeration on 500+ sites using Maigret"""
    
    def validate_input(self, input_data: str) -> tuple[bool, str]:
        """Validate username input"""
        if not input_data or not input_data.strip():
            return False, "Username cannot be empty"
        
        username = input_data.strip()
        if len(username) < 2:
            return False, "Username must be at least 2 characters"
        
        return True, ""
    
    def run(self, input_data: str, api_keys: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Search for username using Maigret CLI
        
        This is a placeholder - requires Maigret installation
        """
        # Check if maigret is installed
        if not shutil.which('maigret'):
            return {
                'success': False,
                'error': 'Maigret is not installed. Install it with: pip install maigret'
            }
        
        return {
            'success': False,
            'error': 'Maigret tool integration coming soon. CLI tool detected but parser not yet implemented.'
        }


class SnoopTool(BaseTool):
    """Username OSINT on many platforms using Snoop"""
    
    def validate_input(self, input_data: str) -> tuple[bool, str]:
        """Validate username input"""
        if not input_data or not input_data.strip():
            return False, "Username cannot be empty"
        return True, ""
    
    def run(self, input_data: str, api_keys: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Search for username using Snoop
        
        This is a placeholder - requires Snoop installation
        """
        return {
            'success': False,
            'error': 'Snoop tool not yet implemented. Requires Snoop installation.'
        }


class EmailHarvesterTool(BaseTool):
    """Scrape emails from search engines"""
    
    def validate_input(self, input_data: str) -> tuple[bool, str]:
        """Validate domain input"""
        if not input_data or not input_data.strip():
            return False, "Domain cannot be empty"
        return True, ""
    
    def run(self, input_data: str, api_keys: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Harvest emails using EmailHarvester CLI
        
        This is a placeholder - requires EmailHarvester and API keys
        """
        if not api_keys or 'emailharvester' not in api_keys:
            return {
                'success': False,
                'error': 'EmailHarvester requires a Bing API key. This tool will prompt for it when available.'
            }
        
        return {
            'success': False,
            'error': 'EmailHarvester tool not yet fully implemented.'
        }
