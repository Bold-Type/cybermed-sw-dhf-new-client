#!/usr/bin/env python3
"""
Debug script to show exactly what files are in the template folder.
This will help identify the caching issue.
"""

import os
import sys
import json

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from drive_client import DriveClient
from colorama import Fore, Style, init

init()

def load_config():
    """Load configuration from settings.json."""
    config_path = os.path.join(os.path.dirname(__file__), "config", "settings.json")
    with open(config_path, 'r') as f:
        return json.load(f)

def print_folder_contents(structure, indent=0):
    """Recursively print folder contents."""
    prefix = "  " * indent
    
    for item in structure.get('children', []):
        if item['type'] == 'folder':
            print(f"{prefix}📁 {Fore.BLUE}{item['name']}{Style.RESET_ALL}")
            print_folder_contents(item, indent + 1)
        else:
            mime_type = item.get('mimeType', 'unknown')
            if 'google-apps' in mime_type:
                print(f"{prefix}📄 {Fore.YELLOW}{item['name']}{Style.RESET_ALL} ({mime_type})")
            else:
                print(f"{prefix}📄 {Fore.GREEN}{item['name']}{Style.RESET_ALL} ({mime_type})")

def main():
    """Debug the template folder contents."""
    print(f"\n{Fore.BLUE}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}  Template Folder Debug - Current Contents{Style.RESET_ALL}")
    print(f"{Fore.BLUE}{'='*60}{Style.RESET_ALL}\n")
    
    try:
        # Load configuration
        config = load_config()
        
        # Create drive client
        drive_client = DriveClient(config)
        
        # Force fresh authentication
        print(f"{Fore.CYAN}🔄 Authenticating with fresh connection...{Style.RESET_ALL}")
        if not drive_client.force_fresh_authentication():
            print(f"{Fore.RED}✗ Authentication failed{Style.RESET_ALL}")
            sys.exit(1)
        
        # Get template folder structure
        print(f"{Fore.CYAN}📁 Reading template folder structure...{Style.RESET_ALL}")
        print(f"Template Folder ID: {config['template_folder_id']}")
        print()
        
        template_structure = drive_client.get_folder_structure(config["template_folder_id"])
        
        if not template_structure:
            print(f"{Fore.RED}✗ Failed to read template structure{Style.RESET_ALL}")
            sys.exit(1)
        
        print(f"{Fore.GREEN}📋 Current Template Contents:{Style.RESET_ALL}")
        print(f"📁 {Fore.BLUE}{template_structure['name']}{Style.RESET_ALL}")
        print_folder_contents(template_structure, 1)
        
        # Count files
        def count_items(structure):
            folders = 0
            files = 0
            for item in structure.get('children', []):
                if item['type'] == 'folder':
                    folders += 1
                    sub_f, sub_files = count_items(item)
                    folders += sub_f
                    files += sub_files
                else:
                    files += 1
            return folders, files
        
        total_folders, total_files = count_items(template_structure)
        print(f"\n{Fore.CYAN}📊 Summary: {total_folders} folders, {total_files} files{Style.RESET_ALL}")
        
        # Highlight specific files user mentioned
        def find_file(structure, filename):
            for item in structure.get('children', []):
                if item['type'] == 'file' and filename in item['name']:
                    return True
                elif item['type'] == 'folder':
                    if find_file(item, filename):
                        return True
            return False
        
        print(f"\n{Fore.YELLOW}🔍 Checking for specific files user mentioned:{Style.RESET_ALL}")
        files_to_check = [
            "James-Hayes-and-Andres-Echeverry_2025-12-16.mp3",
            "James-Hayes-and-Andres-Echeverry-1413cc64-cf71.srt"
        ]
        
        for filename in files_to_check:
            found = find_file(template_structure, filename)
            status = f"{Fore.RED}❌ FOUND (should be removed)" if found else f"{Fore.GREEN}✅ NOT FOUND (correctly removed)"
            print(f"  {filename}: {status}{Style.RESET_ALL}")
        
        print(f"\n{Fore.GREEN}Debug complete!{Style.RESET_ALL}\n")
        
    except Exception as e:
        print(f"{Fore.RED}✗ Error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()
