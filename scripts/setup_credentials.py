#!/usr/bin/env python3
"""
One-time setup script for storing Google Service Account credentials.
Stores credentials securely in system keyring (macOS Keychain, Windows Credential Store, etc.)
"""

import json
import os
import sys
from pathlib import Path
from colorama import Fore, Style, init

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from auth.credential_manager import CredentialManager

# Initialize colorama for cross-platform colored output
init()

def print_header():
    """Print application header."""
    print(f"\n{Fore.BLUE}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}  CyberMed Software DHF - Credential Setup{Style.RESET_ALL}")
    print(f"{Fore.BLUE}{'='*70}{Style.RESET_ALL}\n")

def get_credentials_file_path() -> Path:
    """Get the path to the service account credentials file."""
    while True:
        try:
            print(f"{Fore.CYAN}Enter the path to your service account JSON file:{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}(You can drag and drop the file into the terminal){Style.RESET_ALL}")
            
            file_path = input("Path: ").strip()
            
            # Remove quotes if dragged and dropped
            file_path = file_path.strip("'\"")
            
            # Expand user home directory
            file_path = os.path.expanduser(file_path)
            
            path = Path(file_path)
            
            if not path.exists():
                print(f"{Fore.RED}✗ File not found: {file_path}{Style.RESET_ALL}")
                continue
            
            if not path.is_file():
                print(f"{Fore.RED}✗ Not a file: {file_path}{Style.RESET_ALL}")
                continue
            
            if not file_path.lower().endswith('.json'):
                print(f"{Fore.RED}✗ File must be a .json file{Style.RESET_ALL}")
                continue
            
            return path
            
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Operation cancelled by user{Style.RESET_ALL}")
            sys.exit(0)

def validate_service_account_file(file_path: Path) -> str:
    """Validate and read the service account credentials file."""
    try:
        with open(file_path, 'r') as f:
            credentials_data = f.read()
        
        # Parse JSON to validate format
        credentials_dict = json.loads(credentials_data)
        
        # Check for required fields
        required_fields = ['type', 'client_email', 'private_key', 'project_id']
        missing_fields = [field for field in required_fields if field not in credentials_dict]
        
        if missing_fields:
            print(f"{Fore.RED}✗ Missing required fields: {', '.join(missing_fields)}{Style.RESET_ALL}")
            return None
        
        if credentials_dict.get('type') != 'service_account':
            print(f"{Fore.RED}✗ Invalid credential type. Expected 'service_account', got '{credentials_dict.get('type')}'{Style.RESET_ALL}")
            return None
        
        print(f"{Fore.GREEN}✓ Valid service account credentials file{Style.RESET_ALL}")
        print(f"  Project ID: {credentials_dict['project_id']}")
        print(f"  Client Email: {credentials_dict['client_email']}")
        
        return credentials_data
        
    except FileNotFoundError:
        print(f"{Fore.RED}✗ File not found: {file_path}{Style.RESET_ALL}")
        return None
    except json.JSONDecodeError as e:
        print(f"{Fore.RED}✗ Invalid JSON file: {str(e)}{Style.RESET_ALL}")
        return None
    except Exception as e:
        print(f"{Fore.RED}✗ Error reading file: {str(e)}{Style.RESET_ALL}")
        return None

def confirm_storage(credentials_dict: dict) -> bool:
    """Confirm with user before storing credentials."""
    print(f"\n{Fore.YELLOW}Ready to store credentials securely:{Style.RESET_ALL}")
    print(f"  Project: {credentials_dict['project_id']}")
    print(f"  Service Account: {credentials_dict['client_email']}")
    
    while True:
        confirm = input(f"\nProceed with storing credentials? (y/n): ").strip().lower()
        if confirm in ['y', 'yes']:
            return True
        elif confirm in ['n', 'no']:
            return False
        else:
            print(f"{Fore.YELLOW}Please enter 'y' for yes or 'n' for no{Style.RESET_ALL}")

def main():
    """Main function for credential setup."""
    try:
        print_header()
        
        # Initialize credential manager
        credential_manager = CredentialManager()
        
        # Show keyring information
        keyring_info = credential_manager.get_keyring_info()
        print(f"Keyring Backend: {keyring_info['keyring_backend']}")
        print(f"Platform: {keyring_info['platform']}\n")
        
        # Check if credentials already exist
        if credential_manager.check_credentials_exist():
            print(f"{Fore.YELLOW}⚠ Credentials already exist in keyring{Style.RESET_ALL}")
            
            while True:
                overwrite = input("Overwrite existing credentials? (y/n): ").strip().lower()
                if overwrite in ['y', 'yes']:
                    break
                elif overwrite in ['n', 'no']:
                    print(f"{Fore.CYAN}Keeping existing credentials. Setup cancelled.{Style.RESET_ALL}")
                    sys.exit(0)
                else:
                    print(f"{Fore.YELLOW}Please enter 'y' for yes or 'n' for no{Style.RESET_ALL}")
        
        # Get credentials file path
        credentials_file = get_credentials_file_path()
        
        # Validate and read credentials file
        credentials_json = validate_service_account_file(credentials_file)
        if not credentials_json:
            print(f"{Fore.RED}✗ Failed to validate credentials file{Style.RESET_ALL}")
            sys.exit(1)
        
        # Parse for confirmation
        credentials_dict = json.loads(credentials_json)
        
        # Confirm with user
        if not confirm_storage(credentials_dict):
            print(f"{Fore.YELLOW}Setup cancelled by user{Style.RESET_ALL}")
            sys.exit(0)
        
        # Store credentials
        if credential_manager.store_credentials(credentials_json):
            print(f"\n{Fore.GREEN}🎉 Credentials stored successfully!{Style.RESET_ALL}")
            print(f"{Fore.CYAN}You can now run: python scripts/create_workspace.py{Style.RESET_ALL}")
            print(f"\n{Fore.YELLOW}Note: Your credentials are stored securely in the system keyring.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}The original JSON file can be safely deleted if desired.{Style.RESET_ALL}\n")
        else:
            print(f"{Fore.RED}✗ Failed to store credentials{Style.RESET_ALL}")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Setup cancelled by user{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}✗ Unexpected error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()
