"""
Files & Metadata OSINT Tools
Implements tools for file analysis and metadata extraction
"""

from tools.base_tool import BaseTool
from typing import Dict, Any, Optional
import subprocess
import shutil
import os


class ExiftoolTool(BaseTool):
    """Extract metadata from images, videos, documents using exiftool"""
    
    def validate_input(self, input_data: str) -> tuple[bool, str]:
        """Validate file path input"""
        if not input_data or not input_data.strip():
            return False, "File path cannot be empty"
        
        file_path = input_data.strip()
        if not os.path.exists(file_path):
            return False, f"File does not exist: {file_path}"
        
        if not os.path.isfile(file_path):
            return False, f"Path is not a file: {file_path}"
        
        return True, ""
    
    def run(self, input_data: str, api_keys: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Extract metadata using exiftool CLI
        
        Requires exiftool installation
        """
        file_path = input_data.strip()
        
        if not shutil.which('exiftool'):
            return {
                'success': False,
                'error': 'exiftool is not installed. Download from: https://exiftool.org/'
            }
        
        try:
            # Run exiftool with JSON output
            result = subprocess.run(
                ['exiftool', '-j', file_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                return {
                    'success': False,
                    'error': f'exiftool failed: {result.stderr}'
                }
            
            # Parse JSON output
            import json
            try:
                metadata = json.loads(result.stdout)
                if not metadata or len(metadata) == 0:
                    return {
                        'success': False,
                        'error': 'No metadata found in file'
                    }
                
                # Get first item (exiftool returns array)
                data = metadata[0]
                
                # Extract key information
                result_data = {
                    'File Name': data.get('FileName', 'Unknown'),
                    'File Type': data.get('FileType', 'Unknown'),
                    'File Size': data.get('FileSize', 'Unknown'),
                    'MIME Type': data.get('MIMEType', 'Unknown'),
                    'Image Size': data.get('ImageSize', 'N/A'),
                    'Megapixels': data.get('Megapixels', 'N/A'),
                    'Camera Make': data.get('Make', 'N/A'),
                    'Camera Model': data.get('Model', 'N/A'),
                    'Date/Time': data.get('DateTimeOriginal', data.get('CreateDate', 'N/A')),
                    'GPS Position': data.get('GPSPosition', 'N/A'),
                    'Software': data.get('Software', 'N/A'),
                    'Author': data.get('Author', data.get('Artist', 'N/A'))
                }
                
                return {
                    'success': True,
                    'data': result_data
                }
                
            except json.JSONDecodeError:
                return {
                    'success': False,
                    'error': 'Failed to parse exiftool output'
                }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'exiftool timed out after 30 seconds'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'exiftool error: {str(e)}'
            }


class PefileTool(BaseTool):
    """Analyze PE files (Windows executables)"""
    
    def validate_input(self, input_data: str) -> tuple[bool, str]:
        """Validate file path input"""
        if not input_data or not input_data.strip():
            return False, "File path cannot be empty"
        
        file_path = input_data.strip()
        if not os.path.exists(file_path):
            return False, f"File does not exist: {file_path}"
        
        return True, ""
    
    def run(self, input_data: str, api_keys: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Analyze PE file structure using pefile library
        """
        file_path = input_data.strip()
        
        try:
            import pefile
            
            # Parse PE file
            pe = pefile.PE(file_path)
            
            # Extract key information
            result_data = {
                'File': os.path.basename(file_path),
                'Machine Type': hex(pe.FILE_HEADER.Machine),
                'Number of Sections': pe.FILE_HEADER.NumberOfSections,
                'Time Date Stamp': pe.FILE_HEADER.dump_dict().get('TimeDateStamp', {}).get('Value', 'N/A'),
                'Entry Point': hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint),
                'Image Base': hex(pe.OPTIONAL_HEADER.ImageBase),
                'Subsystem': pe.OPTIONAL_HEADER.Subsystem,
                'DLL Characteristics': hex(pe.OPTIONAL_HEADER.DllCharacteristics),
                'Sections': ', '.join([s.Name.decode('utf-8', errors='ignore').rstrip('\x00') 
                                      for s in pe.sections]),
                'Imported DLLs': len(pe.DIRECTORY_ENTRY_IMPORT) if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT') else 0
            }
            
            pe.close()
            
            return {
                'success': True,
                'data': result_data
            }
            
        except ImportError:
            return {
                'success': False,
                'error': 'pefile library not installed. Run: pip install pefile'
            }
        except pefile.PEFormatError:
            return {
                'success': False,
                'error': 'File is not a valid PE file'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'PE file analysis error: {str(e)}'
            }


class YaraTool(BaseTool):
    """Pattern-based file scanning using YARA"""
    
    def validate_input(self, input_data: str) -> tuple[bool, str]:
        """Validate file path input"""
        if not input_data or not input_data.strip():
            return False, "File path cannot be empty"
        return True, ""
    
    def run(self, input_data: str, api_keys: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Scan file using YARA rules
        
        This is a placeholder - requires YARA installation and rules
        """
        return {
            'success': False,
            'error': 'YARA tool not yet implemented. Requires YARA installation and rule configuration.'
        }
