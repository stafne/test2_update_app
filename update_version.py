#!/usr/bin/env python3
"""
Script to update version numbers in version.py and setup.py
"""

import re
import sys

def update_version(new_version):
    # Update version.py
    with open('version.py', 'r') as f:
        content = f.read()
    
    content = re.sub(r'__version__ = "[^"]*"', f'__version__ = "{new_version}"', content)
    
    with open('version.py', 'w') as f:
        f.write(content)
    
    print(f'Updated version.py to {new_version}')
    
    # Update setup.py
    with open('setup.py', 'r') as f:
        content = f.read()
    
    content = re.sub(r"'CFBundleVersion': '[^']*'", f"'CFBundleVersion': '{new_version}'", content)
    content = re.sub(r"'CFBundleShortVersionString': '[^']*'", f"'CFBundleShortVersionString': '{new_version}'", content)
    
    with open('setup.py', 'w') as f:
        f.write(content)
    
    print(f'Updated setup.py to {new_version}')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 update_version.py <new_version>")
        sys.exit(1)
    
    new_version = sys.argv[1]
    update_version(new_version)
