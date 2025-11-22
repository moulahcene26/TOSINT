"""
Domains & Infrastructure OSINT Tools
Implements tools for domain enumeration and infrastructure analysis
"""

from tools.base_tool import BaseTool
from typing import Dict, Any, Optional
import subprocess
import shutil
import socket


class TheHarvesterTool(BaseTool):
    """Emails, subdomains, hosts from search engines using theHarvester"""
    
    def validate_input(self, input_data: str) -> tuple[bool, str]:
        """Validate domain input"""
        if not input_data or not input_data.strip():
            return False, "Domain cannot be empty"
        
        domain = input_data.strip()
        if ' ' in domain:
            return False, "Domain cannot contain spaces"
        
        return True, ""
    
    def run(self, input_data: str, api_keys: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Harvest information using theHarvester CLI
        
        Requires theHarvester installation
        """
        if not shutil.which('theHarvester'):
            return {
                'success': False,
                'error': 'theHarvester is not installed. Install it with: pip install theHarvester'
            }
        
        return {
            'success': False,
            'error': 'theHarvester tool integration coming soon. CLI detected but parser not yet implemented.'
        }


class Sublist3rTool(BaseTool):
    """Subdomain enumeration using Sublist3r"""
    
    def validate_input(self, input_data: str) -> tuple[bool, str]:
        """Validate domain input"""
        if not input_data or not input_data.strip():
            return False, "Domain cannot be empty"
        
        domain = input_data.strip()
        if ' ' in domain:
            return False, "Domain cannot contain spaces"
        
        return True, ""
    
    def run(self, input_data: str, api_keys: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Enumerate subdomains using Sublist3r
        
        This tool uses Python import if available
        """
        domain = input_data.strip()
        
        try:
            import sublist3r
            
            # Run Sublist3r
            subdomains = sublist3r.main(
                domain,
                40,  # threads
                None,  # savefile
                ports=None,
                silent=True,
                verbose=False,
                enable_bruteforce=False,
                engines=None
            )
            
            if not subdomains:
                return {
                    'success': True,
                    'data': {
                        'Domain': domain,
                        'Subdomains Found': 0,
                        'Status': 'No subdomains discovered'
                    }
                }
            
            return {
                'success': True,
                'data': {
                    'Domain': domain,
                    'Subdomains Found': len(subdomains),
                    'Subdomains': '\n' + '\n'.join([f'  • {sub}' for sub in sorted(subdomains)])
                }
            }
            
        except ImportError:
            return {
                'success': False,
                'error': 'Sublist3r is not installed. Install it with: pip install sublist3r'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Sublist3r error: {str(e)}'
            }


class AmassTool(BaseTool):
    """Deep DNS enumeration & asset discovery using Amass"""
    
    def validate_input(self, input_data: str) -> tuple[bool, str]:
        """Validate domain input"""
        if not input_data or not input_data.strip():
            return False, "Domain cannot be empty"
        return True, ""
    
    def run(self, input_data: str, api_keys: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Perform deep DNS enumeration using Amass CLI
        
        Requires Amass installation
        """
        if not shutil.which('amass'):
            return {
                'success': False,
                'error': 'Amass is not installed. Download from: https://github.com/OWASP/Amass'
            }
        
        return {
            'success': False,
            'error': 'Amass tool integration coming soon. CLI detected but parser not yet implemented.'
        }


class DNSReconTool(BaseTool):
    """DNS enumeration using dnsrecon"""
    
    def validate_input(self, input_data: str) -> tuple[bool, str]:
        """Validate domain input"""
        if not input_data or not input_data.strip():
            return False, "Domain cannot be empty"
        return True, ""
    
    def run(self, input_data: str, api_keys: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Perform DNS enumeration using dnsrecon CLI
        
        Requires dnsrecon installation
        """
        if not shutil.which('dnsrecon'):
            return {
                'success': False,
                'error': 'dnsrecon is not installed. Install it with: pip install dnsrecon'
            }
        
        return {
            'success': False,
            'error': 'dnsrecon tool integration coming soon. CLI detected but parser not yet implemented.'
        }


class NmapTool(BaseTool):
    """Port scanning and network discovery using Nmap"""
    
    def supports_streaming(self) -> bool:
        """Nmap supports streaming output"""
        return True
    
    def validate_input(self, input_data: str) -> tuple[bool, str]:
        """Validate IP/domain input"""
        if not input_data or not input_data.strip():
            return False, "Target (IP or domain) cannot be empty"
        return True, ""
    
    def run_streaming(self, input_data: str, api_keys: Optional[Dict[str, str]] = None):
        """
        Run Nmap with streaming output
        
        Returns:
            subprocess.Popen object
        """
        target = input_data.strip()
        
        # Check if nmap is installed
        if not shutil.which('nmap'):
            raise RuntimeError('Nmap is not installed. Install from: https://nmap.org/download.html')
        
        # Start nmap process with streaming output
        process = subprocess.Popen(
            ['nmap', '-sT', '-F', '--open', '-v', target],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1,
            universal_newlines=False
        )
        
        return process

    
    def run(self, input_data: str, api_keys: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Perform port scan using Nmap
        
        Requires Nmap installation and appropriate permissions
        """
        target = input_data.strip()
        
        if not shutil.which('nmap'):
            return {
                'success': False,
                'error': 'Nmap is not installed. Install from: https://nmap.org/download.html'
            }
        
        try:
            # Simple TCP SYN scan on common ports
            result = subprocess.run(
                ['nmap', '-sT', '-F', '--open', target],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode != 0:
                return {
                    'success': False,
                    'error': f'Nmap scan failed: {result.stderr}'
                }
            
            # Parse output
            output = result.stdout
            lines = output.split('\n')
            
            open_ports = []
            for line in lines:
                if '/tcp' in line and 'open' in line:
                    open_ports.append(line.strip())
            
            if not open_ports:
                return {
                    'success': True,
                    'data': {
                        'Target': target,
                        'Status': 'No open ports found in common port range',
                        'Note': 'Try a more comprehensive scan for detailed results'
                    }
                }
            
            return {
                'success': True,
                'data': {
                    'Target': target,
                    'Open Ports': len(open_ports),
                    'Results': '\n' + '\n'.join([f'  • {port}' for port in open_ports]),
                    'Note': 'Fast scan on common ports only'
                }
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Nmap scan timed out after 120 seconds'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Nmap error: {str(e)}'
            }


class WafW00fTool(BaseTool):
    """WAF fingerprinting using wafw00f"""
    
    def validate_input(self, input_data: str) -> tuple[bool, str]:
        """Validate URL input"""
        if not input_data or not input_data.strip():
            return False, "URL cannot be empty"
        
        url = input_data.strip()
        if not (url.startswith('http://') or url.startswith('https://')):
            return False, "URL must start with http:// or https://"
        
        return True, ""
    
    def run(self, input_data: str, api_keys: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Detect WAF using wafw00f CLI
        
        Requires wafw00f installation
        """
        if not shutil.which('wafw00f'):
            return {
                'success': False,
                'error': 'wafw00f is not installed. Install it with: pip install wafw00f'
            }
        
        url = input_data.strip()
        
        try:
            result = subprocess.run(
                ['wafw00f', url],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            output = result.stdout
            
            # Simple parsing
            if 'No WAF' in output or 'not behind' in output.lower():
                return {
                    'success': True,
                    'data': {
                        'URL': url,
                        'WAF Detected': 'No',
                        'Status': 'No Web Application Firewall detected'
                    }
                }
            
            # Try to extract WAF name
            lines = output.split('\n')
            waf_name = 'Unknown'
            for line in lines:
                if 'detected' in line.lower() or 'behind' in line.lower():
                    waf_name = line.strip()
                    break
            
            return {
                'success': True,
                'data': {
                    'URL': url,
                    'WAF Detected': 'Yes',
                    'Details': waf_name,
                    'Raw Output': output[:500]  # First 500 chars
                }
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'wafw00f scan timed out after 30 seconds'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'wafw00f error: {str(e)}'
            }
