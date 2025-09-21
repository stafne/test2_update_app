"""
Version management for Beautiful Flower Display
"""

__version__ = "1.0.1"
__app_name__ = "Beautiful Flower Display"
__bundle_id__ = "com.yourcompany.flowerapp"

# GitHub repository info for updates
GITHUB_REPO_OWNER = "stafne"  # Your GitHub username
GITHUB_REPO_NAME = "test2_update_app"  # Your actual repo name
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/releases/latest"
DOWNLOAD_URL_TEMPLATE = f"https://github.com/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/releases/download/{{version}}/Beautiful-Flower-Display-{{version}}.dmg"
