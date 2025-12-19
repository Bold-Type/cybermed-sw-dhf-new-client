# Google Workspace Service Account Setup Guide

This guide walks you through creating a Google service account for your Google Workspace organization to enable the automation tool to access your Drive folders.

## Prerequisites

- Google Workspace Admin access (or someone with admin access to help)
- Access to the Google Cloud Console
- Access to the specific Drive folders you want to automate

## Step 1: Create a Google Cloud Project

1. **Go to Google Cloud Console**: https://console.cloud.google.com/
2. **Sign in** with your Google Workspace account
3. **Create a new project** (or use existing one):
   - Click the project dropdown at top
   - Click "NEW PROJECT"
   - Name it something like "CyberMed DHF Automation"
   - Set organization to your Google Workspace org
   - Click "CREATE"

## Step 2: Enable the Google Drive API

1. **Navigate to APIs & Services** > **Library**
2. **Search for "Google Drive API"**
3. **Click on "Google Drive API"**
4. **Click "ENABLE"**

## Step 3: Create a Service Account

1. **Go to IAM & Admin** > **Service Accounts**
2. **Click "CREATE SERVICE ACCOUNT"**
3. **Fill in details**:
   - Service account name: `dhf-automation`
   - Service account ID: `dhf-automation` (auto-filled)
   - Description: `Service account for CyberMed DHF workspace automation`
4. **Click "CREATE AND CONTINUE"**
5. **Skip the role assignment** (we'll handle permissions in Drive directly)
6. **Click "DONE"**

## Step 4: Create Service Account Key

> **Note**: Google may suggest using "Workload Identity Federation" for enhanced security. While this is a more secure approach, it's also more complex to set up. For this automation tool, the traditional service account key approach below is simpler and perfectly adequate for your use case.

1. **Click on your new service account** from the list
2. **Go to the "Keys" tab**
3. **Click "ADD KEY" > "Create new key"**
4. **Select "JSON" format**
5. **Click "CREATE"**
6. **If prompted about security concerns**:
   - Click **"I understand the security implications"** or similar
   - This is normal for service account keys
7. **Download the key file** (keep it secure!)
   - Save it somewhere safe like `~/Downloads/cybermed-dhf-automation.json`
   - This file contains your credentials

## Step 5: Grant Drive Access

### Option A: Individual Folder Permissions (Recommended)

1. **Open Google Drive** (https://drive.google.com)
2. **Navigate to your "Client Folder Template" folder**
3. **Right-click the folder** > **Share**
4. **Add the service account**:
   - Enter the service account email (looks like: `dhf-automation@project-name.iam.gserviceaccount.com`)
   - Grant **Editor** permission
   - **Uncheck "Notify people"** (it's a service account)
   - Click **Share**

5. **Navigate to your "Client Shared Folders" parent folder**
6. **Repeat the sharing process** with **Editor** permission

### Option B: Domain-Wide Delegation (Advanced - Requires Admin)

If you need broader access, your Google Workspace admin can set up domain-wide delegation:

1. **In Google Cloud Console** > **IAM & Admin** > **Service Accounts**
2. **Click your service account**
3. **Click "ENABLE G SUITE DOMAIN-WIDE DELEGATION"**
4. **Note the Client ID** (long number)
5. **Ask your Google Workspace admin** to:
   - Go to Google Admin Console
   - Navigate to Security > API Controls > Domain-wide Delegation
   - Add your Client ID with scope: `https://www.googleapis.com/auth/drive`

## Step 6: Find Your Folder IDs

You need the Google Drive folder IDs for configuration:

### Template Folder ID
1. **Navigate to your "Client Folder Template" in Google Drive**
2. **Look at the URL**: `https://drive.google.com/drive/folders/1HefI6gL2Z3AKmUwZVMBJBk5DogRik6k8`
3. **Copy the ID**: `1HefI6gL2Z3AKmUwZVMBJBk5DogRik6k8`

### Target Parent Folder ID
1. **Navigate to your "Client Shared Folders" in Google Drive**
2. **Look at the URL**: `https://drive.google.com/drive/folders/1ucrox_lDFYas7w1iWx8FaektDr_LR8AK`
3. **Copy the ID**: `1ucrox_lDFYas7w1iWx8FaektDr_LR8AK`

## Step 7: Update Configuration

Update the `config/settings.json` file with your folder IDs:

```json
{
  "template_folder_id": "YOUR_TEMPLATE_FOLDER_ID_HERE",
  "target_parent_folder_id": "YOUR_TARGET_PARENT_FOLDER_ID_HERE",
  "template_name": "Client Folder Template",
  "target_parent_name": "Client Shared Folders",
  "keyring_service": "cybermed-sw-dhf-new-client",
  "keyring_username": "service_account"
}
```

## Step 8: Test the Setup

Once you have the service account JSON file and updated the configuration:

```bash
# Run the credential setup
python scripts/setup_credentials.py

# Test workspace creation
python scripts/create_workspace.py
```

## Troubleshooting

### "Permission denied" errors
- Verify the service account email is shared with Editor permissions on both folders
- Check that the folder IDs are correct in `config/settings.json`

### "API not enabled" errors
- Make sure Google Drive API is enabled in your Google Cloud project
- Wait a few minutes after enabling as it can take time to propagate

### "Authentication failed" errors
- Verify the service account JSON file is valid
- Make sure you downloaded the key in JSON format (not P12)
- Check that the file path is correct when running setup

### Workspace admin help needed
- If you don't have admin access, share this guide with your Google Workspace admin
- They can create the service account and set up domain-wide delegation if needed

## Security Notes

- **Keep the service account key file secure** - it's like a password
- **Don't commit the JSON file to version control** (it's in .gitignore)
- **Consider rotating the key periodically** for enhanced security
- **Use minimum required permissions** - Editor on specific folders only

## Support

If you encounter issues:
1. Check the folder IDs are correct
2. Verify service account permissions
3. Test with a simple folder structure first
4. Review the error messages in the terminal output
