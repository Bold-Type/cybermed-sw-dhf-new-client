"""
Google Drive API client for workspace automation.
Handles authentication, folder operations, and file copying.
"""

import json
import time
from typing import Optional, List, Dict, Any
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.errors import HttpError
from colorama import Fore, Style, init

from auth.credential_manager import CredentialManager

# Initialize colorama for cross-platform colored output
init()

class DriveClient:
    """Google Drive API client with service account authentication."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.credential_manager = CredentialManager(
            service=config["keyring_service"], 
            username=config["keyring_username"]
        )
        self.service = None
        self.scopes = ['https://www.googleapis.com/auth/drive']
    
    def authenticate(self) -> bool:
        """
        Authenticate with Google Drive API using service account credentials.
        
        Returns:
            bool: True if authentication successful, False otherwise
        """
        try:
            # Retrieve credentials from keyring
            credentials_dict = self.credential_manager.retrieve_credentials()
            if not credentials_dict:
                return False
            
            # Create service account credentials
            credentials = service_account.Credentials.from_service_account_info(
                credentials_dict, scopes=self.scopes
            )
            
            # Build the Drive API service
            self.service = build('drive', 'v3', credentials=credentials)
            
            # Test the connection
            self.service.about().get(fields="user").execute()
            
            print(f"{Fore.GREEN}✓ Successfully authenticated with Google Drive API{Style.RESET_ALL}")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}✗ Authentication failed: {str(e)}{Style.RESET_ALL}")
            return False
    
    def get_folder_structure(self, folder_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the complete folder structure and contents.
        
        Args:
            folder_id: Google Drive folder ID
            
        Returns:
            Dict: Folder structure with files and subfolders
        """
        try:
            if not self.service:
                raise Exception("Not authenticated. Call authenticate() first.")
            
            # Get folder metadata (with Shared Drive support)
            folder_metadata = self.service.files().get(
                fileId=folder_id, 
                fields="id,name,mimeType",
                supportsAllDrives=True
            ).execute()
            
            structure = {
                'id': folder_metadata['id'],
                'name': folder_metadata['name'],
                'type': 'folder',
                'children': []
            }
            
            # Get all items in the folder (with Shared Drive support)
            query = f"'{folder_id}' in parents and trashed=false"
            results = self.service.files().list(
                q=query,
                fields="files(id,name,mimeType,parents)",
                orderBy="folder,name",
                supportsAllDrives=True,
                includeItemsFromAllDrives=True
            ).execute()
            
            items = results.get('files', [])
            
            for item in items:
                if item['mimeType'] == 'application/vnd.google-apps.folder':
                    # Recursively get subfolder structure
                    subfolder = self.get_folder_structure(item['id'])
                    if subfolder:
                        structure['children'].append(subfolder)
                else:
                    # Add file to structure
                    structure['children'].append({
                        'id': item['id'],
                        'name': item['name'],
                        'type': 'file',
                        'mimeType': item['mimeType']
                    })
            
            return structure
            
        except HttpError as e:
            print(f"{Fore.RED}✗ HTTP Error getting folder structure: {e}{Style.RESET_ALL}")
            return None
        except Exception as e:
            print(f"{Fore.RED}✗ Error getting folder structure: {str(e)}{Style.RESET_ALL}")
            return None
    
    def create_folder(self, name: str, parent_id: str) -> Optional[str]:
        """
        Create a new folder in Google Drive.
        
        Args:
            name: Name of the new folder
            parent_id: Parent folder ID
            
        Returns:
            str: ID of created folder or None if failed
        """
        try:
            if not self.service:
                raise Exception("Not authenticated. Call authenticate() first.")
            
            file_metadata = {
                'name': name,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [parent_id]
            }
            
            folder = self.service.files().create(
                body=file_metadata, 
                fields='id',
                supportsAllDrives=True
            ).execute()
            folder_id = folder.get('id')
            
            print(f"{Fore.CYAN}✓ Created folder: {name}{Style.RESET_ALL}")
            return folder_id
            
        except HttpError as e:
            print(f"{Fore.RED}✗ HTTP Error creating folder '{name}': {e}{Style.RESET_ALL}")
            return None
        except Exception as e:
            print(f"{Fore.RED}✗ Error creating folder '{name}': {str(e)}{Style.RESET_ALL}")
            return None
    
    def copy_file(self, source_file_id: str, new_name: str, destination_folder_id: str) -> Optional[str]:
        """
        Copy a file to a new location.
        
        Args:
            source_file_id: ID of file to copy
            new_name: Name for the copied file
            destination_folder_id: Destination folder ID
            
        Returns:
            str: ID of copied file or None if failed
        """
        try:
            if not self.service:
                raise Exception("Not authenticated. Call authenticate() first.")
            
            file_metadata = {
                'name': new_name,
                'parents': [destination_folder_id]
            }
            
            copied_file = self.service.files().copy(
                fileId=source_file_id,
                body=file_metadata,
                fields='id',
                supportsAllDrives=True
            ).execute()
            
            copied_file_id = copied_file.get('id')
            print(f"{Fore.CYAN}✓ Copied file: {new_name}{Style.RESET_ALL}")
            return copied_file_id
            
        except HttpError as e:
            print(f"{Fore.RED}✗ HTTP Error copying file '{new_name}': {e}{Style.RESET_ALL}")
            return None
        except Exception as e:
            print(f"{Fore.RED}✗ Error copying file '{new_name}': {str(e)}{Style.RESET_ALL}")
            return None
    
    def replicate_structure(self, source_structure: Dict[str, Any], target_parent_id: str, 
                          client_name: str) -> Optional[str]:
        """
        Replicate a folder structure in a new location.
        
        Args:
            source_structure: Source folder structure from get_folder_structure()
            target_parent_id: Parent folder ID for the new structure
            client_name: Name of the client (used for main folder name)
            
        Returns:
            str: ID of the created client folder or None if failed
        """
        try:
            if not self.service:
                raise Exception("Not authenticated. Call authenticate() first.")
            
            print(f"{Fore.BLUE}Creating workspace structure for {client_name}...{Style.RESET_ALL}")
            
            # Create main client folder
            client_folder_id = self.create_folder(client_name, target_parent_id)
            if not client_folder_id:
                return None
            
            # Replicate the template structure inside the client folder
            self._replicate_folder_contents(source_structure, client_folder_id)
            
            print(f"{Fore.GREEN}✓ Workspace creation completed for {client_name}{Style.RESET_ALL}")
            return client_folder_id
            
        except Exception as e:
            print(f"{Fore.RED}✗ Error replicating structure: {str(e)}{Style.RESET_ALL}")
            return None
    
    def _replicate_folder_contents(self, source_structure: Dict[str, Any], target_folder_id: str):
        """
        Recursively replicate folder contents.
        
        Args:
            source_structure: Source folder structure
            target_folder_id: Target folder ID
        """
        for item in source_structure.get('children', []):
            if item['type'] == 'folder':
                # Create subfolder
                new_folder_id = self.create_folder(item['name'], target_folder_id)
                if new_folder_id:
                    # Recursively replicate subfolder contents
                    self._replicate_folder_contents(item, new_folder_id)
            else:
                # Copy file
                self.copy_file(item['id'], item['name'], target_folder_id)
                # Add small delay to avoid rate limiting
                time.sleep(0.1)
    
    def test_access(self) -> bool:
        """
        Test access to the configured folders.
        
        Returns:
            bool: True if access test successful, False otherwise
        """
        try:
            if not self.service:
                print(f"{Fore.YELLOW}⚠ Not authenticated{Style.RESET_ALL}")
                return False
            
            # Test access to template folder (with Shared Drive support)
            template_folder_id = self.config["template_folder_id"]
            template_folder = self.service.files().get(
                fileId=template_folder_id, 
                fields="id,name",
                supportsAllDrives=True
            ).execute()
            
            # Test access to target parent folder (with Shared Drive support)
            target_folder_id = self.config["target_parent_folder_id"]
            target_folder = self.service.files().get(
                fileId=target_folder_id, 
                fields="id,name",
                supportsAllDrives=True
            ).execute()
            
            print(f"{Fore.GREEN}✓ Access verified:{Style.RESET_ALL}")
            print(f"  Template: {template_folder['name']}")
            print(f"  Target: {target_folder['name']}")
            
            return True
            
        except HttpError as e:
            print(f"{Fore.RED}✗ Access test failed: {e}{Style.RESET_ALL}")
            return False
        except Exception as e:
            print(f"{Fore.RED}✗ Error testing access: {str(e)}{Style.RESET_ALL}")
            return False
