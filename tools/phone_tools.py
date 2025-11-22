"""
Phone Numbers Tools - OSINT tools for phone number analysis
"""

from typing import Dict, Any, Optional
from tools.base_tool import BaseTool
import phonenumbers
from phonenumbers import geocoder, carrier, timezone


class PhoneNumbersTool(BaseTool):
    """Phone number parsing and validation using phonenumbers library"""
    
    def validate_input(self, input_data: str) -> tuple[bool, str]:
        """
        Validate phone number input
        
        Args:
            input_data: Phone number string
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not input_data or not input_data.strip():
            return False, "Phone number cannot be empty"
        
        # Remove common formatting characters for basic validation
        cleaned = input_data.strip().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        
        if len(cleaned) < 7:
            return False, "Phone number seems too short"
        
        return True, ""
    
    def run(self, input_data: str, api_keys: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Parse and analyze phone number
        
        Args:
            input_data: Phone number string (with or without country code)
            api_keys: Not used for this tool
            
        Returns:
            Dictionary with phone number information
        """
        try:
            # Try to parse the number
            # If no country code provided, try common regions
            parsed_number = None
            original_input = input_data.strip()
            
            # Try to parse with explicit country code first
            if original_input.startswith('+'):
                try:
                    parsed_number = phonenumbers.parse(original_input, None)
                except:
                    pass
            
            # If no success, try common regions
            if parsed_number is None:
                for region in ['US', 'GB', 'CA', 'AU', 'DE', 'FR', 'IN', 'CN']:
                    try:
                        parsed_number = phonenumbers.parse(original_input, region)
                        if phonenumbers.is_valid_number(parsed_number):
                            break
                    except:
                        continue
            
            if parsed_number is None:
                return {
                    'success': False,
                    'error': 'Could not parse phone number. Please include country code (e.g., +1 for US)'
                }
            
            # Check if valid
            is_valid = phonenumbers.is_valid_number(parsed_number)
            is_possible = phonenumbers.is_possible_number(parsed_number)
            
            # Get additional information
            country = geocoder.description_for_number(parsed_number, "en")
            carrier_name = carrier.name_for_number(parsed_number, "en")
            timezones = timezone.time_zones_for_number(parsed_number)
            
            # Format in different styles
            formatted_international = phonenumbers.format_number(
                parsed_number, 
                phonenumbers.PhoneNumberFormat.INTERNATIONAL
            )
            formatted_national = phonenumbers.format_number(
                parsed_number,
                phonenumbers.PhoneNumberFormat.NATIONAL
            )
            formatted_e164 = phonenumbers.format_number(
                parsed_number,
                phonenumbers.PhoneNumberFormat.E164
            )
            
            # Number type
            number_type = phonenumbers.number_type(parsed_number)
            type_names = {
                0: "Fixed Line",
                1: "Mobile",
                2: "Fixed Line or Mobile",
                3: "Toll Free",
                4: "Premium Rate",
                5: "Shared Cost",
                6: "VoIP",
                7: "Personal Number",
                8: "Pager",
                9: "UAN (Universal Access Number)",
                10: "Voicemail",
                99: "Unknown"
            }
            type_str = type_names.get(number_type, "Unknown")
            
            result_data = {
                'Original Input': original_input,
                'Valid': 'Yes' if is_valid else 'No',
                'Possible': 'Yes' if is_possible else 'No',
                'Country/Region': country if country else 'Unknown',
                'Carrier': carrier_name if carrier_name else 'Unknown',
                'Number Type': type_str,
                'Timezones': ', '.join(timezones) if timezones else 'Unknown',
                'International Format': formatted_international,
                'National Format': formatted_national,
                'E.164 Format': formatted_e164,
                'Country Code': f"+{parsed_number.country_code}",
                'National Number': str(parsed_number.national_number)
            }
            
            return {
                'success': True,
                'data': result_data
            }
            
        except phonenumbers.NumberParseException as e:
            return {
                'success': False,
                'error': f'Parse error: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}'
            }
    
    def get_input_prompt(self) -> str:
        """Get input prompt for phone number"""
        return "Enter phone number (include country code, e.g., +1234567890):"


class NumverifyTool(BaseTool):
    """Phone validation using Numverify API"""
    
    def validate_input(self, input_data: str) -> tuple[bool, str]:
        """Validate phone number input"""
        if not input_data or not input_data.strip():
            return False, "Phone number cannot be empty"
        return True, ""
    
    def run(self, input_data: str, api_keys: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Run Numverify API call"""
        # This will be implemented when we add API support
        return {
            'success': False,
            'error': 'Numverify API integration not yet implemented'
        }


class TruecallerTool(BaseTool):
    """Unofficial Truecaller number lookup"""
    
    def validate_input(self, input_data: str) -> tuple[bool, str]:
        """Validate phone number input"""
        if not input_data or not input_data.strip():
            return False, "Phone number cannot be empty"
        return True, ""
    
    def run(self, input_data: str, api_keys: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Run Truecaller lookup"""
        # This will be implemented in later iterations
        return {
            'success': False,
            'error': 'Truecaller integration not yet implemented'
        }
