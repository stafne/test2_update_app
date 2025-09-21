"""
Auto-update functionality for Beautiful Flower Display
"""

import requests
import json
import tkinter as tk
from tkinter import messagebox
import webbrowser
import threading
from packaging import version
from version import __version__, GITHUB_API_URL, DOWNLOAD_URL_TEMPLATE


class UpdateChecker:
    def __init__(self, parent_window=None):
        self.parent_window = parent_window
        self.current_version = __version__
    
    def check_for_updates(self, show_no_update_message=False):
        """Check for updates in a background thread"""
        def _check():
            try:
                response = requests.get(GITHUB_API_URL, timeout=10)
                if response.status_code == 200:
                    release_data = response.json()
                    latest_version = release_data['tag_name'].lstrip('v')
                    
                    if version.parse(latest_version) > version.parse(self.current_version):
                        self._show_update_dialog(latest_version, release_data)
                    elif show_no_update_message:
                        self._show_no_update_message()
                else:
                    if show_no_update_message:
                        error_msg = f"Failed to check for updates (HTTP {response.status_code})"
                        if response.status_code == 404:
                            error_msg += "\n\nThis usually means:\n• No releases exist yet\n• Repository is private\n• Repository doesn't exist"
                        self._show_error_message(error_msg)
            except Exception as e:
                if show_no_update_message:
                    self._show_error_message(f"Update check failed: {str(e)}")
        
        # Run check in background thread
        thread = threading.Thread(target=_check, daemon=True)
        thread.start()
    
    def _show_update_dialog(self, latest_version, release_data):
        """Show update available dialog"""
        def _show_dialog():
            title = "Update Available"
            message = f"""A new version of Beautiful Flower Display is available!

Current version: {self.current_version}
Latest version: {latest_version}

Release Notes:
{release_data.get('body', 'No release notes available')[:200]}...

Would you like to download the update?"""
            
            result = messagebox.askyesno(title, message, parent=self.parent_window)
            if result:
                download_url = f"https://github.com/{GITHUB_API_URL.split('/')[4]}/{GITHUB_API_URL.split('/')[5]}/releases/tag/v{latest_version}"
                webbrowser.open(download_url)
        
        # Show dialog on main thread
        if self.parent_window:
            self.parent_window.after(0, _show_dialog)
        else:
            _show_dialog()
    
    def _show_no_update_message(self):
        """Show no update available message"""
        def _show_dialog():
            messagebox.showinfo(
                "No Updates", 
                f"You're running the latest version ({self.current_version})",
                parent=self.parent_window
            )
        
        if self.parent_window:
            self.parent_window.after(0, _show_dialog)
        else:
            _show_dialog()
    
    def _show_error_message(self, error):
        """Show error message"""
        def _show_dialog():
            messagebox.showerror(
                "Update Check Failed", 
                error,
                parent=self.parent_window
            )
        
        if self.parent_window:
            self.parent_window.after(0, _show_dialog)
        else:
            _show_dialog()


def check_for_updates_startup(parent_window=None):
    """Check for updates on app startup (silent)"""
    checker = UpdateChecker(parent_window)
    checker.check_for_updates(show_no_update_message=False)


def check_for_updates_manual(parent_window=None):
    """Manual update check (shows result)"""
    checker = UpdateChecker(parent_window)
    checker.check_for_updates(show_no_update_message=True)
