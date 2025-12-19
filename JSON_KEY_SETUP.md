# JSON Key File Setup - Quick Guide

## 🔐 Secure Credential Storage

**Important**: The JSON key file is **NOT stored in the project folder**. Instead, our tool uses your system's secure keyring (macOS Keychain) for maximum security.

## How It Works

1. **Download JSON key** from Google Cloud Console (step 4 in GOOGLE_SETUP_GUIDE.md)
2. **Save it temporarily** somewhere safe like:
   - `~/Downloads/cybermed-dhf-automation.json`
   - Desktop
   - Any temporary location
3. **Run the setup script** which reads the file and stores credentials securely:
   ```bash
   python scripts/setup_credentials.py
   ```
4. **The script will prompt you** for the file path:
   ```
   Enter the path to your service account JSON file:
   (You can drag and drop the file into the terminal)
   Path: 
   ```
5. **Drag and drop or type the path** to your downloaded JSON file
6. **Credentials are stored securely** in macOS Keychain
7. **Delete the JSON file** for security (optional but recommended)

## Example Workflow

```bash
# Step 1: Download JSON from Google Cloud Console
# Save to ~/Downloads/cybermed-dhf-automation.json

# Step 2: Run setup script
cd /Users/andresecheverry/github-bold-type/cybermed-sw-dhf-new-client
python scripts/setup_credentials.py

# Step 3: When prompted, drag and drop the file or type:
# Path: ~/Downloads/cybermed-dhf-automation.json

# Step 4: Script stores credentials securely
# ✓ Credentials stored securely in Darwin keyring

# Step 5: Delete the JSON file (optional)
rm ~/Downloads/cybermed-dhf-automation.json
```

## Security Benefits

- ✅ **No credentials in project folder**
- ✅ **No risk of accidentally committing secrets**  
- ✅ **Encrypted storage in macOS Keychain**
- ✅ **Cross-platform compatible** (Windows Credential Store, Linux KDE Wallet)
- ✅ **One-time setup** - never need the JSON file again

## File Locations (What goes where)

```
cybermed-sw-dhf-new-client/
├── config/settings.json          # ✅ Folder IDs (safe to commit)
├── src/                          # ✅ Source code (safe to commit) 
├── scripts/                      # ✅ Scripts (safe to commit)
└── .gitignore                    # ✅ Prevents JSON files from being committed

~/Downloads/                      # ⚠️ Temporary location for JSON file
└── cybermed-dhf-automation.json  # ❌ Delete after setup
```

## Once Setup Is Complete

After running `python scripts/setup_credentials.py` successfully:

- ✅ Credentials are in macOS Keychain
- ✅ Run workspace creation: `python scripts/create_workspace.py`  
- ✅ JSON file can be safely deleted
- ✅ Team members clone repo and run their own credential setup

## If You Need Help

Run the credential setup script and follow the prompts:
```bash
python scripts/setup_credentials.py
```

The script will guide you through the process step by step!
