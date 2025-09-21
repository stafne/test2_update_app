# GitHub Auto-Update Integration Guide

This guide explains how to set up and use GitHub-based auto-updates for your Beautiful Flower Display app.

## How It Works

1. **Version Checking**: The app checks GitHub's API for the latest release
2. **Update Detection**: Compares current version with latest release version
3. **User Notification**: Shows update dialog if newer version is available
4. **Download**: Opens GitHub release page for user to download new version

## Setup Instructions

### 1. Initial GitHub Repository Setup

1. **Push your code to GitHub** (if not already done):
   ```bash
   git add .
   git commit -m "Initial commit with auto-update functionality"
   git push origin main
   ```

2. **Create your first release**:
   ```bash
   # Use the provided script
   ./create_release.sh
   # Or manually:
   git tag v1.0.0
   git push origin v1.0.0
   ```

### 2. GitHub Actions Setup

The `.github/workflows/release.yml` file will automatically:
- Build your macOS app when you create a new tag
- Create a DMG file
- Upload it to the GitHub release

**No additional setup required** - GitHub Actions will work automatically once you push the workflow file.

### 3. Testing the Update Mechanism

1. **Test with current version**:
   ```bash
   python flower_app.py
   ```
   Click "🔄 Check Updates" - should show "You're running the latest version"

2. **Create a test update**:
   ```bash
   # Update version to 1.0.1
   ./create_release.sh
   # Enter: 1.0.1
   ```

3. **Test the update detection**:
   - Run the app again
   - Click "🔄 Check Updates"
   - Should show update available dialog

## Creating New Releases

### Method 1: Using the Script (Recommended)
```bash
./create_release.sh
```
Follow the prompts to enter the new version number.

### Method 2: Manual Process
1. Update `version.py`:
   ```python
   __version__ = "1.0.2"  # New version
   ```

2. Update `setup.py`:
   ```python
   'CFBundleVersion': '1.0.2',
   'CFBundleShortVersionString': '1.0.2',
   ```

3. Commit and tag:
   ```bash
   git add version.py setup.py
   git commit -m "Bump version to 1.0.2"
   git tag v1.0.2
   git push origin main
   git push origin v1.0.2
   ```

## How Users Get Updates

1. **Automatic Check**: App checks for updates 2 seconds after startup (silent)
2. **Manual Check**: Users can click "🔄 Check Updates" button
3. **Update Dialog**: If update available, shows dialog with:
   - Current vs latest version
   - Release notes
   - Download button
4. **Download**: Opens GitHub release page in browser
5. **Installation**: User downloads and installs new DMG manually

## File Structure

```
├── flower_app.py          # Main app with update UI
├── updater.py            # Update checking logic
├── version.py            # Version info and GitHub config
├── setup.py              # App packaging configuration
├── build_release.sh      # Local build script
├── create_release.sh     # Release creation script
├── .github/workflows/    # GitHub Actions automation
└── UPDATE_GUIDE.md       # This guide
```

## Configuration

### GitHub Repository Settings
Update `version.py` with your repository details:
```python
GITHUB_REPO_OWNER = "yourusername"
GITHUB_REPO_NAME = "your-repo-name"
```

### Update Check Behavior
- **Startup check**: Silent, no dialog if no updates
- **Manual check**: Shows result dialog
- **Network timeout**: 10 seconds
- **Error handling**: Graceful fallback with error messages

## Troubleshooting

### Update Check Fails
- Check internet connection
- Verify GitHub repository name in `version.py`
- Check if repository is public
- Verify release exists on GitHub

### Build Fails
- Ensure all dependencies are installed
- Check Python version compatibility
- Verify py2app is working
- Check GitHub Actions logs

### App Won't Start
- Check all dependencies in `requirements.txt`
- Verify Python path
- Check for missing modules

## Security Considerations

- **Code signing**: Consider code signing your app for macOS
- **HTTPS**: All GitHub API calls use HTTPS
- **User consent**: Updates require explicit user approval
- **No automatic installation**: Users must manually install updates

## Future Enhancements

1. **Automatic installation**: Implement automatic DMG mounting and installation
2. **Delta updates**: Only download changed files
3. **Rollback capability**: Allow reverting to previous versions
4. **Background updates**: Download updates in background
5. **Code signing**: Add proper macOS code signing

## Support

For issues with the update mechanism:
1. Check GitHub Actions logs
2. Verify repository settings
3. Test with a simple version bump
4. Check network connectivity
