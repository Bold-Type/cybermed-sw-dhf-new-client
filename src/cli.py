"""
CLI interface for CyberMed Software DHF New Client workspace creation.
Main user interface for creating client workspaces.
"""

import json
import os
import sys
from typing import Dict, Any
from colorama import Fore, Style, init

from .drive_client import DriveClient
from .auth.credential_manager import CredentialManager

# Initialize colorama for cross-platform colored output
init()

class WorkspaceCreatorCLI:
    """Command line interface for workspace creation."""
    
    def __init__(self):
        self.config = self._load_config()
        self.drive_client = DriveClient(self.config)
        self.credential_manager = CredentialManager(
            service=self.config["keyring_service"],
            username=self.config["keyring_username"]
        )
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from settings.json."""
        try:
            # Get the directory containing this script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(script_dir, "..", "config", "settings.json")
            config_path = os.path.normpath(config_path)
            
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            return config
            
        except FileNotFoundError:
            print(f"{Fore.RED}✗ Configuration file not found: {config_path}{Style.RESET_ALL}")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"{Fore.RED}✗ Invalid JSON in configuration file{Style.RESET_ALL}")
            sys.exit(1)
        except Exception as e:
            print(f"{Fore.RED}✗ Error loading configuration: {str(e)}{Style.RESET_ALL}")
            sys.exit(1)
    
    def _print_header(self):
        """Print application header."""
        print(f"\n{Fore.BLUE}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}  CyberMed Software DHF - New Client Workspace Creator{Style.RESET_ALL}")
        print(f"{Fore.BLUE}{'='*60}{Style.RESET_ALL}\n")
    
    def _check_prerequisites(self) -> bool:
        """Check if all prerequisites are met."""
        print(f"{Fore.YELLOW}Checking prerequisites...{Style.RESET_ALL}")
        
        # Check if credentials are stored
        if not self.credential_manager.check_credentials_exist():
            print(f"{Fore.RED}✗ No credentials found in keyring{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Please run: python scripts/setup_credentials.py{Style.RESET_ALL}")
            return False
        
        # Test authentication
        if not self.drive_client.authenticate():
            print(f"{Fore.RED}✗ Authentication failed{Style.RESET_ALL}")
            return False
        
        # Test access to folders
        if not self.drive_client.test_access():
            print(f"{Fore.RED}✗ Cannot access required folders{Style.RESET_ALL}")
            return False
        
        print(f"{Fore.GREEN}✓ All prerequisites met{Style.RESET_ALL}\n")
        return True
    
    def _get_client_name(self) -> str:
        """Get client name from user input with validation."""
        while True:
            try:
                client_name = input(f"{Fore.CYAN}Enter client name: {Style.RESET_ALL}").strip()
                
                if not client_name:
                    print(f"{Fore.RED}✗ Client name cannot be empty{Style.RESET_ALL}")
                    continue
                
                # Basic validation
                if len(client_name) > 50:
                    print(f"{Fore.RED}✗ Client name too long (max 50 characters){Style.RESET_ALL}")
                    continue
                
                # Confirm with user
                print(f"\nCreating workspace for: {Fore.GREEN}{client_name}{Style.RESET_ALL}")
                confirm = input(f"Is this correct? (y/n): ").strip().lower()
                
                if confirm in ['y', 'yes']:
                    return client_name
                elif confirm in ['n', 'no']:
                    continue
                else:
                    print(f"{Fore.YELLOW}Please enter 'y' for yes or 'n' for no{Style.RESET_ALL}")
                    
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Operation cancelled by user{Style.RESET_ALL}")
                sys.exit(0)
            except EOFError:
                print(f"\n{Fore.YELLOW}Operation cancelled{Style.RESET_ALL}")
                sys.exit(0)
    
    def _create_workspace(self, client_name: str) -> bool:
        """Create the client workspace."""
        try:
            print(f"\n{Fore.BLUE}Starting workspace creation...{Style.RESET_ALL}")
            
            # Get template folder structure
            print(f"{Fore.YELLOW}Reading template structure...{Style.RESET_ALL}")
            template_structure = self.drive_client.get_folder_structure(
                self.config["template_folder_id"]
            )
            
            if not template_structure:
                print(f"{Fore.RED}✗ Failed to read template structure{Style.RESET_ALL}")
                return False
            
            print(f"{Fore.GREEN}✓ Template structure loaded{Style.RESET_ALL}")
            
            # Create the client workspace
            client_folder_id = self.drive_client.replicate_structure(
                template_structure,
                self.config["target_parent_folder_id"],
                client_name
            )
            
            if client_folder_id:
                print(f"\n{Fore.GREEN}🎉 Workspace created successfully!{Style.RESET_ALL}")
                print(f"{Fore.CYAN}Client folder ID: {client_folder_id}{Style.RESET_ALL}")
                return True
            else:
                print(f"\n{Fore.RED}✗ Failed to create workspace{Style.RESET_ALL}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}✗ Error creating workspace: {str(e)}{Style.RESET_ALL}")
            return False
    
    def run(self):
        """Run the CLI application."""
        try:
            self._print_header()
            
            # Check prerequisites
            if not self._check_prerequisites():
                sys.exit(1)
            
            # Get client name
            client_name = self._get_client_name()
            
            # Create workspace
            success = self._create_workspace(client_name)
            
            if success:
                print(f"\n{Fore.GREEN}✅ All done! Your client workspace is ready.{Style.RESET_ALL}")
                print(f"{Fore.CYAN}You can now access the {client_name} folder in Google Drive.{Style.RESET_ALL}\n")
                sys.exit(0)
            else:
                print(f"\n{Fore.RED}❌ Workspace creation failed.{Style.RESET_ALL}")
                sys.exit(1)
                
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Operation cancelled by user{Style.RESET_ALL}")
            sys.exit(0)
        except Exception as e:
            print(f"\n{Fore.RED}✗ Unexpected error: {str(e)}{Style.RESET_ALL}")
            sys.exit(1)

def main():
    """Entry point for the CLI application."""
    app = WorkspaceCreatorCLI()
    app.run()

if __name__ == "__main__":
    main()
