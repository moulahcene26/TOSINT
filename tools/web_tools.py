"""
Web & URLs OSINT Tools
Implements tools for web and URL analysis
"""

from tools.base_tool import BaseTool
from typing import Dict, Any, Optional
from datetime import datetime


class WaybackpyTool(BaseTool):
    """Archive.org Wayback Machine wrapper using waybackpy"""
    
    def validate_input(self, input_data: str) -> tuple[bool, str]:
        """Validate URL input"""
        if not input_data or not input_data.strip():
            return False, "URL cannot be empty"
        
        # Basic URL validation
        url = input_data.strip()
        if not (url.startswith('http://') or url.startswith('https://')):
            return False, "URL must start with http:// or https://"
        
        return True, ""
    
    def run(self, input_data: str, api_keys: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Query the Wayback Machine for URL snapshots
        
        Args:
            input_data: URL to query
            api_keys: Not used for this tool
            
        Returns:
            Dictionary with archive information
        """
        try:
            from waybackpy import WaybackMachineCDXServerAPI
            
            url = input_data.strip()
            user_agent = "TOSINT - Terminal OSINT Framework"
            
            # Query the Wayback Machine
            cdx_api = WaybackMachineCDXServerAPI(url, user_agent)
            
            # Get snapshots
            snapshots = []
            snapshot_count = 0
            
            for snapshot in cdx_api.snapshots():
                snapshot_count += 1
                if snapshot_count <= 10:  # Limit to first 10 for display
                    snapshots.append({
                        'timestamp': snapshot.datetime_timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                        'status_code': snapshot.statuscode,
                        'archive_url': snapshot.archive_url
                    })
                
                if snapshot_count >= 100:  # Stop after 100 to avoid long processing
                    break
            
            if not snapshots:
                return {
                    'success': True,
                    'data': {
                        'message': f'No archived snapshots found for {url}',
                        'url': url
                    }
                }
            
            # Build output
            result = {
                'URL': url,
                'Total Snapshots Found': str(snapshot_count),
                'Latest 10 Snapshots': '\n\n' + self._format_snapshots(snapshots)
            }
            
            return {
                'success': True,
                'data': result
            }
            
        except ImportError:
            return {
                'success': False,
                'error': 'waybackpy library not installed. Run: pip install waybackpy'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Error querying Wayback Machine: {str(e)}"
            }
    
    def _format_snapshots(self, snapshots: list) -> str:
        """Format snapshots for display"""
        output = []
        for i, snap in enumerate(snapshots, 1):
            output.append(f"[cyan]{i}.[/cyan] {snap['timestamp']} (Status: {snap['status_code']})")
            output.append(f"   {snap['archive_url']}\n")
        return "\n".join(output)


class WhatWebTool(BaseTool):
    """Fingerprint web technologies"""
    
    def validate_input(self, input_data: str) -> tuple[bool, str]:
        """Validate URL input"""
        if not input_data or not input_data.strip():
            return False, "URL cannot be empty"
        return True, ""
    
    def run(self, input_data: str, api_keys: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Fingerprint web technologies using WhatWeb (CLI tool)
        
        This is a placeholder - requires WhatWeb to be installed
        """
        return {
            'success': False,
            'error': 'WhatWeb tool not yet implemented. Requires WhatWeb CLI installation.'
        }


class AquatoneTool(BaseTool):
    """Web reconnaissance with screenshots"""
    
    def validate_input(self, input_data: str) -> tuple[bool, str]:
        """Validate domain/URL input"""
        if not input_data or not input_data.strip():
            return False, "Domain/URL cannot be empty"
        return True, ""
    
    def run(self, input_data: str, api_keys: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Perform web reconnaissance using Aquatone (CLI tool)
        
        This is a placeholder - requires Aquatone to be installed
        """
        return {
            'success': False,
            'error': 'Aquatone tool not yet implemented. Requires Aquatone CLI installation.'
        }


class PhotonTool(BaseTool):
    """Web crawler for extracting URLs, emails, files"""
    
    def validate_input(self, input_data: str) -> tuple[bool, str]:
        """Validate URL input"""
        if not input_data or not input_data.strip():
            return False, "URL cannot be empty"
        return True, ""
    
    def run(self, input_data: str, api_keys: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Crawl website using Photon (CLI tool)
        
        This is a placeholder - requires Photon to be installed
        """
        return {
            'success': False,
            'error': 'Photon tool not yet implemented. Requires Photon CLI installation.'
        }
