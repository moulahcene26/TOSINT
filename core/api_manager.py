"""
API Key Manager - Handle API key storage and retrieval
Stores keys in ~/Documents/TOSINT/.config/api_keys.json
"""

import json
import os
from pathlib import Path
from typing import Optional, Dict


class APIManager:
    """Manage API keys for OSINT tools"""
    
    def __init__(self):
        """Initialize API manager and ensure config directory exists"""
        self.config_dir = Path.home() / "Documents" / "TOSINT" / ".config"
        self.api_keys_file = self.config_dir / "api_keys.json"
        self._ensure_config_exists()
        
    def _ensure_config_exists(self) -> None:
        """Create config directory and file if they don't exist"""
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            if not self.api_keys_file.exists():
                self._save_keys({})
        except Exception as e:
            print(f"Error creating config directory: {e}")
    
    def _load_keys(self) -> Dict[str, str]:
        """
        Load API keys from file
        
        Returns:
            Dictionary of API keys
        """
        try:
            if self.api_keys_file.exists():
                with open(self.api_keys_file, 'r') as f:
                    return json.load(f)
            return {}
        except json.JSONDecodeError:
            return {}
        except Exception as e:
            print(f"Error loading API keys: {e}")
            return {}
    
    def _save_keys(self, keys: Dict[str, str]) -> bool:
        """
        Save API keys to file
        
        Args:
            keys: Dictionary of API keys
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(self.api_keys_file, 'w') as f:
                json.dump(keys, f, indent=2)
            # Set file permissions to read/write for owner only
            os.chmod(self.api_keys_file, 0o600)
            return True
        except Exception as e:
            print(f"Error saving API keys: {e}")
            return False
    
    def get_key(self, service_name: str) -> Optional[str]:
        """
        Get API key for a specific service
        
        Args:
            service_name: Name of the service (e.g., "shodan", "censys")
            
        Returns:
            API key string or None if not found
        """
        keys = self._load_keys()
        return keys.get(service_name.lower())
    
    def set_key(self, service_name: str, api_key: str) -> bool:
        """
        Set API key for a specific service
        
        Args:
            service_name: Name of the service
            api_key: The API key to store
            
        Returns:
            True if successful, False otherwise
        """
        keys = self._load_keys()
        keys[service_name.lower()] = api_key
        return self._save_keys(keys)
    
    def has_key(self, service_name: str) -> bool:
        """
        Check if API key exists for a service
        
        Args:
            service_name: Name of the service
            
        Returns:
            True if key exists, False otherwise
        """
        return self.get_key(service_name) is not None
    
    def delete_key(self, service_name: str) -> bool:
        """
        Delete API key for a specific service
        
        Args:
            service_name: Name of the service
            
        Returns:
            True if successful, False otherwise
        """
        keys = self._load_keys()
        if service_name.lower() in keys:
            del keys[service_name.lower()]
            return self._save_keys(keys)
        return False
    
    def list_services(self) -> list[str]:
        """
        List all services with stored API keys
        
        Returns:
            List of service names
        """
        keys = self._load_keys()
        return list(keys.keys())
    
    def validate_key_format(self, service_name: str, api_key: str) -> tuple[bool, str]:
        """
        Basic validation of API key format
        
        Args:
            service_name: Name of the service
            api_key: The API key to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Basic validation
        if not api_key or not api_key.strip():
            return False, "API key cannot be empty"
        
        if len(api_key) < 10:
            return False, "API key seems too short"
        
        # Service-specific validation
        service_lower = service_name.lower()
        
        if service_lower == "shodan":
            if len(api_key) != 32:
                return False, "Shodan API keys are 32 characters long"
        
        elif service_lower == "censys":
            if ":" not in api_key:
                return False, "Censys requires API_ID:API_SECRET format"
        
        return True, ""
