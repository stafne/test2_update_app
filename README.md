# Beautiful Flower Display App 🌸

A simple, elegant Python application that displays an animated flower. Perfect for packaging as a standalone macOS application with auto-update capabilities.

## Features

- 🌺 Beautiful animated flower with rotating and scaling petals
- 🎨 Colorful petals with smooth animations
- ⏸️ Pause/resume animation controls
- 🌻 Generate new flower variations
- 🖥️ Native macOS app support

## Requirements

- Python 3.7+
- macOS (for building standalone app)

## Installation & Running

1. **Set up virtual environment:**
   ```bash
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app:**
   ```bash
   python flower_app.py
   ```

## Building Standalone macOS App

To create a standalone `.app` bundle that can be distributed:

```bash
# Install dependencies
pip install -r requirements.txt

# Build the app
python setup.py py2app

# The app will be created in the dist/ folder
open dist/
```

## App Structure

- `flower_app.py` - Main application file
- `setup.py` - Configuration for building macOS app
- `requirements.txt` - Python dependencies
- `README.md` - This file

## Auto-Update Preparation

The app is structured to support auto-update functionality:

- Version tracking is built into the app (`version = "1.0.0"`)
- Clean separation of UI and logic
- Proper app bundle configuration in `setup.py`

For implementing auto-updates, consider using:
- **Sparkle framework** (most popular for macOS)
- **py-updater** (Python-specific solution)
- **Custom update mechanism** using GitHub releases

## Customization

You can easily customize:
- Flower colors (modify the `colors` array in `draw_petal()`)
- Animation speed (change the delay in `animate_flower()`)
- Petal count (modify `num_petals` in `draw_flower()`)
- Window size and styling

## License

MIT License - Feel free to use and modify as needed.
