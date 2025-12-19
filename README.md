# CyberMed Software DHF - New Client Workspace Creator

Automated Google Drive workspace creation tool for CyberMed Software DHF client projects. Replicates a standardized template folder structure for new clients with all necessary SOPs and documents.

## Features

- 🚀 **Automated Workspace Creation**: One-click creation of complete client folder structures
- 🔒 **Secure Credential Management**: Cross-platform secure storage using system keyring (macOS Keychain, Windows Credential Store)
- 🌐 **Google Drive API Integration**: Pure cloud-to-cloud operations via Google Drive API
- 🎯 **Dynamic Template Source**: Uses configurable "Client Folder Template" - no hard-coded structures
- 🖥️ **Cross-Platform**: Works on macOS, Windows, and Linux
- 📋 **Interactive CLI**: Simple command-line interface with validation and confirmation

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Cloud Project with Drive API enabled
- Service Account with access to your Google Drive shared folders

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Bold-Type/cybermed-sw-dhf-new-client.git
   cd cybermed-sw-dhf-new-client
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup credentials** (one-time):
   ```bash
   python scripts/setup_credentials.py
   ```
   - Follow prompts to securely store your service account credentials
   - Credentials are stored in your system's secure keyring (Keychain/Credential Store)

4. **Create a client workspace**:
   ```bash
   python scripts/create_workspace.py
   ```
   - Enter client name when prompted
   - Watch as the complete workspace structure is created automatically

## Project Structure

```
cybermed-sw-dhf-new-client/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── .gitignore                         # Git ignore rules
├── config/
│   └── settings.json                  # Configuration (folder IDs, etc.)
├── src/
│   ├── __init__.py
│   ├── auth/
│   │   ├── __init__.py
│   │   └── credential_manager.py      # Keyring credential management
│   ├── drive_client.py               # Google Drive API wrapper
│   └── cli.py                        # Main CLI interface
└── scripts/
    ├── setup_credentials.py          # One-time credential setup
    └── create_workspace.py           # Main workspace creation script
```

## Configuration

The tool reads from `config/settings.json`:

```json
{
  "template_folder_id": "1HefI6gL2Z3AKmUwZVMBJBk5DogRik6k8",
  "target_parent_folder_id": "1ucrox_lDFYas7w1iWx8FaektDr_LR8AK",
  "template_name": "Client Folder Template",
  "target_parent_name": "Client Shared Folders"
}
```

- **template_folder_id**: Google Drive ID of the template folder to replicate
- **target_parent_folder_id**: Parent folder where new client folders will be created
- **keyring_service**: Service name for credential storage (defaults to project name)
- **keyring_username**: Username for credential storage

## How It Works

### Template-Based Replication

1. **Reads Template Structure**: Dynamically discovers the current "Client Folder Template" structure via Google Drive API
2. **Creates Client Folder**: Creates a new folder named after your client
3. **Replicates Structure**: Recursively copies all folders and files from the template
4. **Preserves Templates**: Copies all Google Docs, Sheets, and other files with original names

### Security & Credentials

The tool uses **service account authentication** with credentials stored securely:

- **macOS**: Stored in Keychain
- **Windows**: Stored in Credential Store
- **Linux**: Stored in Secret Service/KDE Wallet

No credentials are ever stored in the repository or configuration files.

## Usage Examples

### Create a New Client Workspace

```bash
$ python scripts/create_workspace.py

============================================================
  CyberMed Software DHF - New Client Workspace Creator
============================================================

Checking prerequisites...
✓ Retrieved credentials from Darwin keyring
✓ Successfully authenticated with Google Drive API
✓ Access verified:
  Template: Client Folder Template
  Target: Client Shared Folders
✓ All prerequisites met

Enter client name: DynoCardia

Creating workspace for: DynoCardia
Is this correct? (y/n): y

Starting workspace creation...
Reading template structure...
✓ Template structure loaded
Creating workspace structure for DynoCardia...
✓ Created folder: DynoCardia
✓ Created folder: 1. Presentations
✓ Created folder: 2. Input Files From Client
✓ Created folder: 3. CyberMed Deliverables
✓ Created folder: Software DHF
✓ Created folder: SOP's
✓ Created folder: Cybermed SOP-01 QMS Software Validation
✓ Copied file: Cybermed SOP-01 QMS Software Validation.gdoc
✓ Copied file: Cybermed SOP-01 Template - QMS Software Validation.gdoc
...

🎉 Workspace created successfully!
Client folder ID: 1ABcDeFgHiJkLmNoPqRsTuVwXyZ

✅ All done! Your client workspace is ready.
You can now access the DynoCardia folder in Google Drive.
```

### Setup Credentials (First Time)

```bash
$ python scripts/setup_credentials.py

======================================================================
  CyberMed Software DHF - Credential Setup
======================================================================

Keyring Backend: keyring.backends.macOS.Keyring
Platform: Darwin

Enter the path to your service account JSON file:
(You can drag and drop the file into the terminal)
Path: ~/Downloads/cybermed-service-account.json

✓ Valid service account credentials file
  Project ID: cybermed-dhf-automation
  Client Email: dhf-automation@cybermed-dhf-automation.iam.gserviceaccount.com

Ready to store credentials securely:
  Project: cybermed-dhf-automation
  Service Account: dhf-automation@cybermed-dhf-automation.iam.gserviceaccount.com

Proceed with storing credentials? (y/n): y

✓ Credentials stored securely in Darwin keyring

🎉 Credentials stored successfully!
You can now run: python scripts/create_workspace.py

Note: Your credentials are stored securely in the system keyring.
The original JSON file can be safely deleted if desired.
```

## Google Cloud Setup

### 1. Create a Service Account

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select or create a project
3. Enable the Google Drive API
4. Go to **IAM & Admin** > **Service Accounts**
5. Click **Create Service Account**
6. Fill in details and click **Create and Continue**
7. Skip role assignment (we'll handle permissions in Drive)
8. Click **Done**

### 2. Create Service Account Key

1. Click on your new service account
2. Go to the **Keys** tab
3. Click **Add Key** > **Create new key**
4. Select **JSON** format
5. Download the key file (keep it secure!)

### 3. Grant Drive Access

1. Open Google Drive and navigate to your shared folders
2. Share both the "Client Folder Template" and "Client Shared Folders" with your service account email
3. Grant **Editor** permission

## Development

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Testing

The tool includes comprehensive error handling and user-friendly feedback. Test your setup by:

1. Running credential setup with a test service account
2. Creating a test client workspace
3. Verifying the structure matches your template

## Troubleshooting

### Common Issues

**❌ Authentication Failed**
- Check that your service account JSON file is valid
- Verify the service account has access to the shared Drive folders
- Confirm Google Drive API is enabled in your Google Cloud project

**❌ Cannot Access Required Folders**
- Ensure the folder IDs in `config/settings.json` are correct
- Verify the service account has Editor permissions on both template and target folders
- Check that the folders exist and are not deleted

**❌ No Credentials Found in Keyring**
- Run `python scripts/setup_credentials.py` first
- On Linux, ensure you have a keyring backend installed (`python -c "import keyring; print(keyring.get_keyring())"`)

**❌ Template Structure Not Found**
- Verify the template_folder_id in config/settings.json
- Check that the "Client Folder Template" folder exists and is accessible
- Ensure the service account has read access to the template folder

### Getting Help

1. Check this README for setup instructions
2. Verify your Google Cloud and Drive permissions
3. Test with a simple folder structure first
4. Check the terminal output for specific error messages

## License

Copyright © 2025 Bold Type. All rights reserved.

## Support

For support, please contact the development team or create an issue in this repository.
