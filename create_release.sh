#!/bin/bash
set -e

echo "🌸 Creating new release for Beautiful Flower Display..."

# Get current version
CURRENT_VERSION=$(python3 -c "from version import __version__; print(__version__)")
echo "Current version: $CURRENT_VERSION"

# Prompt for new version
read -p "Enter new version (current: $CURRENT_VERSION): " NEW_VERSION

if [ -z "$NEW_VERSION" ]; then
    echo "No version entered. Exiting."
    exit 1
fi

# Update version files
echo "Updating version files..."
python3 update_version.py "$NEW_VERSION"

# Commit changes
echo "Committing version changes..."
git add version.py setup.py
git commit -m "Bump version to $NEW_VERSION"

# Create and push tag
echo "Creating and pushing tag v$NEW_VERSION..."
git tag "v$NEW_VERSION"
git push origin main
git push origin "v$NEW_VERSION"

echo "✅ Release v$NEW_VERSION created and pushed!"
echo "GitHub Actions will now build and create the release automatically."
echo "Check your repository's Actions tab to monitor the build progress."
