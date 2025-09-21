"""
Setup script for building a standalone macOS application
Run with: python setup.py py2app
"""

from setuptools import setup

APP = ['flower_app.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'iconfile': None,  # You can add a .icns file here later
    'plist': {
        'CFBundleName': 'Beautiful Flower Display',
        'CFBundleDisplayName': 'Beautiful Flower Display',
        'CFBundleGetInfoString': 'A beautiful animated flower display app',
        'CFBundleIdentifier': 'com.yourcompany.flowerapp',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHighResolutionCapable': True,
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    install_requires=['Pillow'],
)
