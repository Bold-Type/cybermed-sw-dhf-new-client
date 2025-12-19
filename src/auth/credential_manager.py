"""
Cross-platform credential management using system keyring.
Securely stores and retrieves Google Service Account credentials.
"""

import json
import keyring
import platform
from typing import Optional, Dict, Any
from colorama import Fore, Style, init

# Initialize colorama for cross-platform colored output
init()

class CredentialManager:
    """Manages Google Service Account credentials using system keyring."""
    
    def __init__(self, service: str = "cybermed-sw-dhf-new-client", username: str = "service_account"):
        self.service = service
        self.username = username
        self.platform = platform.system()
    
    def store_credentials(self, credentials_json: str) -> bool:
        """
        Store service account credentials in system keyring.
        
        Args:
            credentials_json: JSON string of service account credentials
            
        Returns:
            bool: True if stored successfully, False otherwise
        """
        try:
            # Validate JSON format
            json.loads(credentials_json)
            
            # Store in keyring
            keyring.set_password(self.service, self.username, credentials_json)
            
            print(f"{Fore.GREEN}✓ Credentials stored securely in {self.platform} keyring{Style.RESET_ALL}")
            return True
            
        except json.JSONDecodeError:
            print(f"{Fore.RED}✗ Invalid JSON format in credentials{Style.RESET_ALL}")
            return False
        except Exception as e:
            print(f"{Fore.RED}✗ Failed to store credentials: {str(e)}{Style.RESET_ALL}")
            return False
    
    def retrieve_credentials(self) -> Optional[Dict[Any, Any]]:
        """
        Retrieve service account credentials from system keyring.
        
        Returns:
            Dict: Service account credentials or None if not found
        """
        try:
            credentials_json = keyring.get_password(self.service, self.username)
            
            if credentials_json is None:
                print(f"{Fore.YELLOW}⚠ No credentials found in keyring{Style.RESET_ALL}")
                print(f"  Run: {Fore.CYAN}python scripts/setup_credentials.py{Style.RESET_ALL}")
                return None
            
            credentials = json.loads(credentials_json)
            print(f"{Fore.GREEN}✓ Retrieved credentials from {self.platform} keyring{Style.RESET_ALL}")
            return credentials
            
        except json.JSONDecodeError:
            print(f"{Fore.RED}✗ Corrupted credentials in keyring{Style.RESET_ALL}")
            return None
        except Exception as e:
            print(f"{Fore.RED}✗ Failed to retrieve credentials: {str(e)}{Style.RESET_ALL}")
            return None
    
    def delete_credentials(self) -> bool:
        """
        Delete stored credentials from keyring.
        
        Returns:
            bool: True if deleted successfully, False otherwise
        """
        try:
            keyring.delete_password(self.service, self.username)
            print(f"{Fore.GREEN}✓ Credentials deleted from keyring{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}✗ Failed to delete credentials: {str(e)}{Style.RESET_ALL}")
            return False
    
    def check_credentials_exist(self) -> bool:
        """
        Check if credentials are stored in keyring.
        
        Returns:
            bool: True if credentials exist, False otherwise
        """
        try:
            credentials = keyring.get_password(self.service, self.username)
            return credentials is not None
        except Exception:
            return False
    
    def get_keyring_info(self) -> Dict[str, str]:
        """
        Get information about the keyring backend being used.
        
        Returns:
            Dict: Information about keyring backend
        """
        return {
            "platform": self.platform,
            "keyring_backend": str(keyring.get_keyring()),
            "service": self.service,
            "username": self.username
        }
