"""
Network & IP Intelligence OSINT Tools
Implements tools for IP, network, and device intelligence
"""

from tools.base_tool import BaseTool
from typing import Dict, Any, Optional
import requests
import socket


class ShodanTool(BaseTool):
    """IP/device intelligence using Shodan API"""
    
    def validate_input(self, input_data: str) -> tuple[bool, str]:
        """Validate IP address input"""
        if not input_data or not input_data.strip():
            return False, "IP address cannot be empty"
        
        ip = input_data.strip()
        
        # Basic IP validation
        try:
            socket.inet_aton(ip)
            return True, ""
        except socket.error:
            return False, "Invalid IP address format"
    
    def run(self, input_data: str, api_keys: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Query Shodan for IP information
        
        Requires Shodan API key
        """
        if not api_keys or 'shodan' not in api_keys:
            return {
                'success': False,
                'error': 'Shodan API key required. Get one at: https://account.shodan.io/register'
            }
        
        try:
            import shodan
            
            api = shodan.Shodan(api_keys['shodan'])
            ip = input_data.strip()
            
            # Query Shodan
            result = api.host(ip)
            
            # Extract relevant information
            data = {
                'IP Address': result.get('ip_str', ip),
                'Organization': result.get('org', 'Unknown'),
                'Operating System': result.get('os', 'Unknown'),
                'Country': result.get('country_name', 'Unknown'),
                'City': result.get('city', 'Unknown'),
                'ISP': result.get('isp', 'Unknown'),
                'Hostnames': ', '.join(result.get('hostnames', [])) or 'None',
                'Open Ports': ', '.join(str(p) for p in result.get('ports', [])) or 'None',
                'Last Update': result.get('last_update', 'Unknown'),
                'Vulnerabilities': len(result.get('vulns', [])) if result.get('vulns') else 0
            }
            
            return {
                'success': True,
                'data': data
            }
            
        except ImportError:
            return {
                'success': False,
                'error': 'Shodan library not installed. Run: pip install shodan'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Shodan query failed: {str(e)}'
            }


class CensysTool(BaseTool):
    """Internet scanning search engine using Censys API"""
    
    def validate_input(self, input_data: str) -> tuple[bool, str]:
        """Validate IP address input"""
        if not input_data or not input_data.strip():
            return False, "IP address cannot be empty"
        return True, ""
    
    def run(self, input_data: str, api_keys: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Query Censys for IP information
        
        Requires Censys API credentials (API_ID:API_SECRET)
        """
        if not api_keys or 'censys' not in api_keys:
            return {
                'success': False,
                'error': 'Censys API credentials required. Get them at: https://search.censys.io/account/api'
            }
        
        return {
            'success': False,
            'error': 'Censys tool not yet fully implemented. API integration coming soon.'
        }


class IPinfoTool(BaseTool):
    """IP geolocation & ASN information using IPinfo API"""
    
    def validate_input(self, input_data: str) -> tuple[bool, str]:
        """Validate IP address input"""
        if not input_data or not input_data.strip():
            return False, "IP address cannot be empty"
        
        ip = input_data.strip()
        
        # Basic IP validation
        try:
            socket.inet_aton(ip)
            return True, ""
        except socket.error:
            return False, "Invalid IP address format"
    
    def run(self, input_data: str, api_keys: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Query IPinfo for IP geolocation and ASN information
        
        Can work without API key but with rate limits
        """
        ip = input_data.strip()
        
        try:
            # Determine if we have an API key
            token = api_keys.get('ipinfo') if api_keys else None
            
            # Build URL
            if token:
                url = f"https://ipinfo.io/{ip}?token={token}"
            else:
                url = f"https://ipinfo.io/{ip}/json"
            
            # Make request
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Check for error
            if 'error' in data:
                return {
                    'success': False,
                    'error': f"IPinfo error: {data['error'].get('message', 'Unknown error')}"
                }
            
            # Format output
            result = {
                'IP Address': data.get('ip', ip),
                'Hostname': data.get('hostname', 'N/A'),
                'City': data.get('city', 'Unknown'),
                'Region': data.get('region', 'Unknown'),
                'Country': data.get('country', 'Unknown'),
                'Location': data.get('loc', 'Unknown'),
                'Organization': data.get('org', 'Unknown'),
                'Postal': data.get('postal', 'N/A'),
                'Timezone': data.get('timezone', 'Unknown')
            }
            
            return {
                'success': True,
                'data': result
            }
            
        except requests.RequestException as e:
            return {
                'success': False,
                'error': f'IPinfo query failed: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Error: {str(e)}'
            }


class ASNLookupTool(BaseTool):
    """Query ASN information via public APIs"""
    
    def validate_input(self, input_data: str) -> tuple[bool, str]:
        """Validate ASN or IP input"""
        if not input_data or not input_data.strip():
            return False, "ASN or IP address cannot be empty"
        return True, ""
    
    def run(self, input_data: str, api_keys: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Look up ASN information using public APIs
        """
        query = input_data.strip()
        
        try:
            # Use ipapi.co for ASN lookup
            if query.startswith('AS') or query.isdigit():
                # ASN query
                asn = query.replace('AS', '')
                url = f"https://api.bgpview.io/asn/{asn}"
            else:
                # IP query
                url = f"https://api.bgpview.io/ip/{query}"
            
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') == 'error':
                return {
                    'success': False,
                    'error': f"API error: {data.get('status_message', 'Unknown error')}"
                }
            
            # Extract ASN data
            result_data = data.get('data', {})
            
            if 'asn' in result_data:
                # ASN query result
                asn_data = result_data['asn']
                result = {
                    'ASN': f"AS{asn_data.get('asn', 'Unknown')}",
                    'Name': asn_data.get('name', 'Unknown'),
                    'Description': asn_data.get('description_short', 'N/A'),
                    'Country': asn_data.get('country_code', 'Unknown'),
                    'Website': asn_data.get('website', 'N/A'),
                    'Email': ', '.join(asn_data.get('email_contacts', [])) or 'N/A',
                    'Abuse': ', '.join(asn_data.get('abuse_contacts', [])) or 'N/A'
                }
            else:
                # IP query result
                result = {
                    'IP': result_data.get('ip', query),
                    'PTR': result_data.get('ptr_record', 'N/A'),
                    'Prefixes': str(len(result_data.get('prefixes', []))),
                    'ASN': ', '.join([f"AS{p.get('asn', {}).get('asn', 'Unknown')}" 
                                     for p in result_data.get('prefixes', [])]) or 'Unknown'
                }
            
            return {
                'success': True,
                'data': result
            }
            
        except requests.RequestException as e:
            return {
                'success': False,
                'error': f'ASN lookup failed: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Error: {str(e)}'
            }
