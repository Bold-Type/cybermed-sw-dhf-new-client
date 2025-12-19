# Shared Drive (Team Drive) Setup Guide

## The Issue with Shared Drives

If your folders are in a **Shared Drive** (formerly Team Drive), you **cannot share individual folders**. Instead, you need to add the service account as a **member of the entire Shared Drive**.

## How to Fix This

### Step 1: Identify Your Shared Drive

1. **Go to Google Drive** (https://drive.google.com)
2. **Look in the left sidebar** for "Shared drives"
3. **Find the Shared Drive** that contains your folders
4. **Click on it** to open

### Step 2: Add Service Account to Shared Drive

1. **Click the Shared Drive name** to select it
2. **Right-click** → **Manage members** (or look for a "people" icon)
3. **Click "Add members"**
4. **Enter the service account email**: `dhf-automation@bt-dhf-copy.iam.gserviceaccount.com`
5. **Set the role to "Content manager"** or **"Manager"** (Editor won't work - it's a different permission)
6. **Uncheck "Notify people"** 
7. **Click "Send"**

### Step 3: Alternative - Use Direct Sharing

If you can't add to the Shared Drive (admin restrictions), try:

1. **Navigate to each folder individually**:
   - Go to your Client Folder Template folder  
   - Go to your Client Shared Folders folder
2. **Right-click each folder** → **Share**
3. **Add**: `dhf-automation@bt-dhf-copy.iam.gserviceaccount.com`
4. **Set to "Editor"**
5. **Click Share**

## Why This Happens

- **Regular Drive**: You can share individual files/folders
- **Shared Drives**: Controlled at the drive level, not individual items
- **Service Accounts**: Treated differently than regular user accounts

## Test After Setup

Once you've added the service account to the Shared Drive:

```bash
cd /Users/andresecheverry/github-bold-type/cybermed-sw-dhf-new-client
python scripts/create_workspace.py
```

## Common Issues

- **"Content manager" vs "Editor"**: Shared Drives use different permission names
- **Admin restrictions**: Some orgs restrict who can add external accounts
- **Propagation time**: May take a few minutes for permissions to take effect

## If You Need Admin Help

Share this with your Workspace admin:

> "Please add service account `dhf-automation@bt-dhf-copy.iam.gserviceaccount.com` as a **Content Manager** to the Shared Drive containing our Client Folder Template and Client Shared Folders. This is needed for our automation tool to create client workspaces."
