#!/usr/bin/env python3
"""
Beautiful Flower Display App
A simple Python application that displays an animated flower.
Perfect for packaging as a standalone macOS app with auto-update capabilities.
"""

import tkinter as tk
from tkinter import ttk
import math
import random
from PIL import Image, ImageDraw, ImageTk
import threading
import time
from version import __version__, __app_name__
from updater import check_for_updates_startup, check_for_updates_manual

class FlowerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Beautiful Flower Display")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        
        # Center the window on screen
        self.center_window()
        
        # App version for update tracking
        self.version = __version__
        
        # Animation variables
        self.animation_running = True
        self.petal_rotation = 0
        self.petal_scale = 1.0
        self.scale_direction = 1
        
        # Setup UI
        self.setup_ui()
        
        # Start animation
        self.animate_flower()
    
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_label = tk.Label(
            self.root,
            text=f"🌸 {__app_name__} 🌸",
            font=("Helvetica", 24, "bold"),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        title_label.pack(pady=20)
        
        # Version label
        version_label = tk.Label(
            self.root,
            text=f"Version {self.version}",
            font=("Helvetica", 12),
            fg='#bdc3c7',
            bg='#2c3e50'
        )
        version_label.pack()
        
        # Canvas for flower
        self.canvas = tk.Canvas(
            self.root,
            width=400,
            height=400,
            bg='#34495e',
            highlightthickness=0
        )
        self.canvas.pack(pady=30)
        
        # Control buttons frame
        button_frame = tk.Frame(self.root, bg='#2c3e50')
        button_frame.pack(pady=10)
        
        # Buttons
        self.animate_button = tk.Button(
            button_frame,
            text="⏸️ Pause Animation",
            font=("Helvetica", 12),
            bg='#e74c3c',
            fg='white',
            relief='flat',
            padx=20,
            pady=10,
            command=self.toggle_animation
        )
        self.animate_button.pack(side=tk.LEFT, padx=10)
        
        new_flower_button = tk.Button(
            button_frame,
            text="🌻 New Flower",
            font=("Helvetica", 12),
            bg='#f39c12',
            fg='white',
            relief='flat',
            padx=20,
            pady=10,
            command=self.generate_new_flower
        )
        new_flower_button.pack(side=tk.LEFT, padx=10)
        
        check_updates_button = tk.Button(
            button_frame,
            text="🔄 Check Updates",
            font=("Helvetica", 12),
            bg='#3498db',
            fg='white',
            relief='flat',
            padx=20,
            pady=10,
            command=self.check_for_updates
        )
        check_updates_button.pack(side=tk.LEFT, padx=10)
        
        # Create initial flower
        self.generate_new_flower()
        
        # Check for updates on startup (silent)
        self.root.after(2000, lambda: check_for_updates_startup(self.root))
    
    def draw_flower(self):
        """Draw a beautiful flower on the canvas"""
        self.canvas.delete("all")
        
        center_x, center_y = 200, 200
        
        # Draw stem
        self.canvas.create_line(
            center_x, center_y + 50, center_x, center_y + 150,
            fill='#27ae60', width=8, capstyle=tk.ROUND
        )
        
        # Draw leaves
        for i, (leaf_x, leaf_y) in enumerate([(center_x - 30, center_y + 80), (center_x + 30, center_y + 120)]):
            points = []
            for angle in range(0, 360, 10):
                radius = 15 + 10 * math.sin(math.radians(angle * 3))
                x = leaf_x + radius * math.cos(math.radians(angle))
                y = leaf_y + radius * 0.5 * math.sin(math.radians(angle))
                points.extend([x, y])
            
            self.canvas.create_polygon(
                points,
                fill='#2ecc71',
                outline='#27ae60',
                width=2
            )
        
        # Draw flower center
        self.canvas.create_oval(
            center_x - 15, center_y - 15,
            center_x + 15, center_y + 15,
            fill='#f1c40f',
            outline='#f39c12',
            width=2
        )
        
        # Draw animated petals
        num_petals = 8
        for i in range(num_petals):
            angle = (360 / num_petals) * i + self.petal_rotation
            self.draw_petal(center_x, center_y, angle, self.petal_scale)
        
        # Draw small dots in center for detail
        for i in range(8):
            angle = i * 45 + self.petal_rotation * 2
            dot_x = center_x + 8 * math.cos(math.radians(angle))
            dot_y = center_y + 8 * math.sin(math.radians(angle))
            self.canvas.create_oval(
                dot_x - 2, dot_y - 2, dot_x + 2, dot_y + 2,
                fill='#e67e22', outline=''
            )
    
    def draw_petal(self, center_x, center_y, angle, scale):
        """Draw a single petal at the given angle"""
        # Petal dimensions
        petal_length = 40 * scale
        petal_width = 20 * scale
        
        # Calculate petal position
        angle_rad = math.radians(angle)
        tip_x = center_x + petal_length * math.cos(angle_rad)
        tip_y = center_y + petal_length * math.sin(angle_rad)
        
        # Create petal shape points
        side_angle1 = angle_rad + math.pi/6
        side_angle2 = angle_rad - math.pi/6
        
        side1_x = center_x + (petal_length * 0.7) * math.cos(side_angle1)
        side1_y = center_y + (petal_length * 0.7) * math.sin(side_angle1)
        
        side2_x = center_x + (petal_length * 0.7) * math.cos(side_angle2)
        side2_y = center_y + (petal_length * 0.7) * math.sin(side_angle2)
        
        # Draw petal
        points = [center_x, center_y, side1_x, side1_y, tip_x, tip_y, side2_x, side2_y]
        
        # Color variations for different petals
        colors = ['#e91e63', '#9c27b0', '#673ab7', '#3f51b5', '#2196f3', '#00bcd4', '#009688', '#4caf50']
        color = colors[int(angle / 45) % len(colors)]
        
        self.canvas.create_polygon(
            points,
            fill=color,
            outline='#ffffff',
            width=1,
            smooth=True
        )
    
    def animate_flower(self):
        """Animate the flower with rotation and scaling"""
        if self.animation_running:
            # Update rotation
            self.petal_rotation += 2
            if self.petal_rotation >= 360:
                self.petal_rotation = 0
            
            # Update scale with breathing effect
            self.petal_scale += 0.02 * self.scale_direction
            if self.petal_scale >= 1.2:
                self.scale_direction = -1
            elif self.petal_scale <= 0.8:
                self.scale_direction = 1
            
            # Redraw flower
            self.draw_flower()
        
        # Schedule next frame
        self.root.after(50, self.animate_flower)
    
    def toggle_animation(self):
        """Toggle animation on/off"""
        self.animation_running = not self.animation_running
        if self.animation_running:
            self.animate_button.config(text="⏸️ Pause Animation", bg='#e74c3c')
        else:
            self.animate_button.config(text="▶️ Resume Animation", bg='#27ae60')
    
    def generate_new_flower(self):
        """Generate a new flower with random characteristics"""
        # Reset animation parameters with some randomness
        self.petal_rotation = random.randint(0, 360)
        self.petal_scale = random.uniform(0.8, 1.2)
        self.scale_direction = random.choice([-1, 1])
        
        # Redraw immediately
        self.draw_flower()
    
    def check_for_updates(self):
        """Manual update check"""
        check_for_updates_manual(self.root)


def main():
    """Main function to run the flower app"""
    # Create the main window
    root = tk.Tk()
    
    # Set app icon (using emoji for simplicity)
    try:
        # For macOS, set the app to appear in dock properly
        if hasattr(tk, '_default_root'):
            root.createcommand('tk::mac::OpenDocument', lambda *args: None)
    except:
        pass
    
    # Create and run the app
    app = FlowerApp(root)
    
    # Handle window closing
    def on_closing():
        app.animation_running = False
        root.quit()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start the GUI event loop
    root.mainloop()


if __name__ == "__main__":
    main()
