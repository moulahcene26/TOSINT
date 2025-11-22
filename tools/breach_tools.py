"""
Data Breaches & Leaks OSINT Tools
Implements tools for checking compromised credentials and data breaches
"""

from tools.base_tool import BaseTool
from typing import Dict, Any, Optional
import requests
import hashlib
import re


class HaveIBeenPwnedTool(BaseTool):
    """Check if email has been in data breaches using HaveIBeenPwned API"""
    
    def validate_input(self, input_data: str) -> tuple[bool, str]:
        """Validate email address"""
        if not input_data or not input_data.strip():
            return False, "Email address cannot be empty"
        
        email = input_data.strip()
        # Basic email validation
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return False, "Invalid email address format"
        
        return True, ""
    
    def run(self, input_data: str, api_keys: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Check email against HIBP database
        
        Note: HIBP API v3 requires API key for breach searches
        Password checks via Pwned Passwords API work without key
        """
        email = input_data.strip()
        
        # Check if we have API key
        api_key = api_keys.get('haveibeenpwned') if api_keys else None
        
        if not api_key:
            return {
                'success': False,
                'error': 'HaveIBeenPwned API key required. Get one at: https://haveibeenpwned.com/API/Key'
            }
        
        try:
            # Query HIBP API
            url = f'https://haveibeenpwned.com/api/v3/breachedaccount/{email}'
            headers = {
                'hibp-api-key': api_key,
                'User-Agent': 'TOSINT-Framework'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 404:
                return {
                    'success': True,
                    'data': {
                        'Email': email,
                        'Status': 'Good news! No breaches found.',
                        'Breaches': 0
                    }
                }
            
            if response.status_code == 200:
                breaches = response.json()
                
                result_data = {
                    'Email': email,
                    'Status': f'⚠ Found in {len(breaches)} breaches',
                    'Breaches': len(breaches),
                    'Details': []
                }
                
                # List first 10 breaches
                for breach in breaches[:10]:
                    result_data['Details'].append(
                        f"{breach['Name']} ({breach['BreachDate']}) - {breach.get('Description', '')[:100]}"
                    )
                
                if len(breaches) > 10:
                    result_data['Details'].append(f"... and {len(breaches) - 10} more breaches")
                
                return {
                    'success': True,
                    'data': result_data
                }
            
            return {
                'success': False,
                'error': f'HIBP API error: {response.status_code} - {response.text}'
            }
            
        except requests.RequestException as e:
            return {
                'success': False,
                'error': f'Network error: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'HIBP error: {str(e)}'
            }


class DehashedTool(BaseTool):
    """Search leaked credentials using Dehashed API"""
    
    def validate_input(self, input_data: str) -> tuple[bool, str]:
        """Validate search query"""
        if not input_data or not input_data.strip():
            return False, "Search query cannot be empty"
        return True, ""
    
    def run(self, input_data: str, api_keys: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Search Dehashed database for leaked credentials
        
        Requires Dehashed API credentials (email + API key)
        Get API access at: https://dehashed.com/
        """
        query = input_data.strip()
        
        api_key = api_keys.get('dehashed') if api_keys else None
        
        if not api_key:
            return {
                'success': False,
                'error': 'Dehashed API key required. Format: email:apikey\nGet access at: https://dehashed.com/'
            }
        
        # Parse email:apikey format
        if ':' not in api_key:
            return {
                'success': False,
                'error': 'Invalid Dehashed API key format. Use: email:apikey'
            }
        
        try:
            email, key = api_key.split(':', 1)
            
            # Query Dehashed API
            url = 'https://api.dehashed.com/search'
            params = {'query': query}
            auth = (email, key)
            
            response = requests.get(url, params=params, auth=auth, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                entries = data.get('entries', [])
                
                result_data = {
                    'Query': query,
                    'Total Results': data.get('total', 0),
                    'Balance': data.get('balance', 'Unknown'),
                    'Entries': []
                }
                
                # Display first 10 results
                for entry in entries[:10]:
                    result_data['Entries'].append({
                        'Email': entry.get('email', 'N/A'),
                        'Username': entry.get('username', 'N/A'),
                        'Password': entry.get('password', 'N/A')[:20] if entry.get('password') else 'N/A',
                        'Database': entry.get('database_name', 'N/A')
                    })
                
                return {
                    'success': True,
                    'data': result_data
                }
            
            return {
                'success': False,
                'error': f'Dehashed API error: {response.status_code} - {response.text}'
            }
            
        except requests.RequestException as e:
            return {
                'success': False,
                'error': f'Network error: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Dehashed error: {str(e)}'
            }


class BreachDirectoryTool(BaseTool):
    """Search email in leaked databases using Breach-Parse"""
    
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
        Search local breach database using breach-parse tool
        
        This tool requires local breach compilation (Collection #1-5, etc.)
        and the breach-parse tool: https://github.com/hmaverickadams/breach-parse
        """
        return {
            'success': False,
            'error': 'BreachDirectory tool requires local breach database setup.\n' \
                    'Setup instructions: https://github.com/hmaverickadams/breach-parse'
        }
