#!/bin/bash
set -e

echo "🌸 Building Beautiful Flower Display Release..."

# Get version from version.py
VERSION=$(python -c "from version import __version__; print(__version__)")
echo "Version: $VERSION"

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build/ dist/

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Build the app
echo "Building macOS app..."
python setup.py py2app

# Create DMG (requires create-dmg: brew install create-dmg)
echo "Creating DMG..."
APP_NAME="Beautiful Flower Display"
DMG_NAME="Beautiful-Flower-Display-${VERSION}.dmg"

if command -v create-dmg &> /dev/null; then
    create-dmg \
        --volname "${APP_NAME}" \
        --window-pos 200 120 \
        --window-size 600 300 \
        --icon-size 100 \
        --icon "${APP_NAME}.app" 175 120 \
        --hide-extension "${APP_NAME}.app" \
        --app-drop-link 425 120 \
        "${DMG_NAME}" \
        "dist/"
    
    echo "✅ DMG created: ${DMG_NAME}"
else
    echo "⚠️  create-dmg not found. Install with: brew install create-dmg"
    echo "✅ App bundle created in dist/ folder"
fi

echo "🎉 Build complete!"
echo "App location: dist/${APP_NAME}.app"
if [ -f "${DMG_NAME}" ]; then
    echo "DMG location: ${DMG_NAME}"
fi
