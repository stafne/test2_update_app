"""
Auto-update functionality for compiled macOS app bundles
This handles downloading and replacing the .app bundle itself
"""

import requests
import json
import tkinter as tk
from tkinter import messagebox
import webbrowser
import threading
import os
import sys
import shutil
import subprocess
from packaging import version
from version import __version__, GITHUB_API_URL, DOWNLOAD_URL_TEMPLATE


class AppUpdater:
    def __init__(self, parent_window=None):
        self.parent_window = parent_window
        self.current_version = __version__
        self.app_path = self._get_app_path()
    
    def _get_app_path(self):
        """Get the path to the current .app bundle"""
        if getattr(sys, 'frozen', False):
            # Running as compiled app
            return os.path.dirname(sys.executable)
        else:
            # Running as script
            return os.path.dirname(os.path.abspath(__file__))
    
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
        """Show update available dialog with download option"""
        def _show_dialog():
            title = "Update Available"
            message = f"""A new version of Beautiful Flower Display is available!

Current version: {self.current_version}
Latest version: {latest_version}

Release Notes:
{release_data.get('body', 'No release notes available')[:200]}...

Would you like to download and install the update?"""
            
            result = messagebox.askyesno(title, message, parent=self.parent_window)
            if result:
                self._download_and_install_update(latest_version, release_data)
        
        # Show dialog on main thread
        if self.parent_window:
            self.parent_window.after(0, _show_dialog)
        else:
            _show_dialog()
    
    def _download_and_install_update(self, latest_version, release_data):
        """Download and install the new app version"""
        def _download():
            try:
                # Find the DMG download URL
                download_url = None
                for asset in release_data.get('assets', []):
                    if asset['name'].endswith('.dmg'):
                        download_url = asset['browser_download_url']
                        break
                
                if not download_url:
                    self._show_error_message("No DMG file found in the release")
                    return
                
                # Show download progress
                self._show_download_progress()
                
                # Download the DMG
                response = requests.get(download_url, stream=True)
                response.raise_for_status()
                
                dmg_path = f"/tmp/Beautiful-Flower-Display-{latest_version}.dmg"
                with open(dmg_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                # Install the update
                self._install_update(dmg_path, latest_version)
                
            except Exception as e:
                self._show_error_message(f"Download failed: {str(e)}")
        
        # Run download in background thread
        thread = threading.Thread(target=_download, daemon=True)
        thread.start()
    
    def _show_download_progress(self):
        """Show download progress dialog"""
        def _show_dialog():
            progress_window = tk.Toplevel(self.parent_window)
            progress_window.title("Downloading Update")
            progress_window.geometry("400x150")
            progress_window.transient(self.parent_window)
            progress_window.grab_set()
            
            tk.Label(progress_window, text="Downloading update...", font=("Helvetica", 12)).pack(pady=20)
            tk.Label(progress_window, text="Please wait while the update is downloaded.", font=("Helvetica", 10)).pack()
            
            # Center the window
            progress_window.update_idletasks()
            x = (progress_window.winfo_screenwidth() // 2) - (400 // 2)
            y = (progress_window.winfo_screenheight() // 2) - (150 // 2)
            progress_window.geometry(f"400x150+{x}+{y}")
        
        if self.parent_window:
            self.parent_window.after(0, _show_dialog)
    
    def _install_update(self, dmg_path, latest_version):
        """Install the update by mounting DMG and replacing the app"""
        try:
            # Mount the DMG
            mount_result = subprocess.run(['hdiutil', 'attach', dmg_path], 
                                        capture_output=True, text=True)
            
            if mount_result.returncode != 0:
                raise Exception("Failed to mount DMG")
            
            # Find the mounted volume
            mount_path = None
            for line in mount_result.stdout.split('\n'):
                if 'Beautiful Flower Display' in line:
                    mount_path = line.split('\t')[-1]
                    break
            
            if not mount_path:
                raise Exception("Could not find mounted app")
            
            # Copy the new app to Applications folder
            new_app_path = os.path.join(mount_path, "Beautiful Flower Display.app")
            apps_folder = "/Applications"
            target_path = os.path.join(apps_folder, "Beautiful Flower Display.app")
            
            # Remove old app if it exists
            if os.path.exists(target_path):
                shutil.rmtree(target_path)
            
            # Copy new app
            shutil.copytree(new_app_path, target_path)
            
            # Unmount the DMG
            subprocess.run(['hdiutil', 'detach', mount_path], capture_output=True)
            
            # Clean up downloaded DMG
            os.remove(dmg_path)
            
            # Show success message
            self._show_success_message(latest_version)
            
        except Exception as e:
            self._show_error_message(f"Installation failed: {str(e)}")
    
    def _show_success_message(self, latest_version):
        """Show success message and offer to restart"""
        def _show_dialog():
            title = "Update Installed"
            message = f"""Update to version {latest_version} has been installed successfully!

The new version has been installed to /Applications/Beautiful Flower Display.app

Would you like to quit and launch the new version?"""
            
            result = messagebox.askyesno(title, message, parent=self.parent_window)
            if result:
                # Launch the new app
                subprocess.Popen(['open', '/Applications/Beautiful Flower Display.app'])
                # Quit current app
                if self.parent_window:
                    self.parent_window.quit()
        
        if self.parent_window:
            self.parent_window.after(0, _show_dialog)
    
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


def check_for_updates_startup(parent_window=None):
    """Check for updates on app startup (silent)"""
    updater = AppUpdater(parent_window)
    updater.check_for_updates(show_no_update_message=False)


def check_for_updates_manual(parent_window=None):
    """Manual update check (shows result)"""
    updater = AppUpdater(parent_window)
    updater.check_for_updates(show_no_update_message=True)
