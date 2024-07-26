import tkinter as tk
from tkinter import messagebox
from pynput import keyboard
import ctypes

class LockIndicator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Lock Indicator")
        self.root.geometry("250x100")
        self.root.resizable(False, False)  # Prevent resizing

        self.x = 0  # For dragging the window
        self.y = 0  # For dragging the window

        # Initialize theme
        self.theme = "light"
        self.auto_start = False  # Example setting for auto-start
        self.configure_theme()  # Apply initial theme settings

        # Drag functionality
        self.root.bind("<ButtonPress-1>", self.start_move)
        self.root.bind("<B1-Motion>", self.do_move)

        # Create a frame for buttons and labels
        self.control_frame = tk.Frame(self.root, bg=self.colors['bg'])
        self.control_frame.pack(fill=tk.X)

        # Create labels for lock status
        self.caps_label = tk.Label(self.root, text="Caps Lock OFF", bg=self.colors['bg'], fg=self.colors['fg'], font=("Arial", 12))
        self.caps_label.pack(expand=True, fill=tk.BOTH)

        self.num_label = tk.Label(self.root, text="Num Lock OFF", bg=self.colors['bg'], fg=self.colors['fg'], font=("Arial", 12))
        self.num_label.pack(expand=True, fill=tk.BOTH)

        # Update lock status initially
        self.update_lock_status()

        # Keyboard listener for lock status updates
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()

        # Create settings button
        settings_button = tk.Button(self.root, text="Settings", command=self.open_settings, bg=self.colors['bg'], fg=self.colors['fg'])
        settings_button.pack(fill=tk.BOTH)

        # Load last position
        self.load_position()

        # Start main loop
        self.root.mainloop()

    def configure_theme(self):
        """Configure theme colors."""
        themes = {
            "light": {"bg": "lightgrey", "fg": "black"},
            "dark": {"bg": "black", "fg": "white"},
            "blue": {"bg": "#005f73", "fg": "white"},
        }
        self.colors = themes.get(self.theme, themes["light"])

    def play_notification_sound(self):
        """Play a notification sound."""
        ctypes.windll.user32.MessageBeep(0x00000040)  # 0x00000040 is MB_ICONEXCLAMATION

    def update_lock_status(self):
        """Update the lock status labels and play a notification sound."""
        capslock_status = self.get_capslock_status()
        numlock_status = self.get_numlock_status()

        caps_text = f"Caps Lock {'ON' if capslock_status else 'OFF'}"
        num_text = f"Num Lock {'ON' if numlock_status else 'OFF'}"

        if self.caps_label.cget("text") != caps_text:
            self.play_notification_sound()
        if self.num_label.cget("text") != num_text:
            self.play_notification_sound()

        self.caps_label.config(text=caps_text, bg=self.colors['bg'], fg=self.colors['fg'])
        self.num_label.config(text=num_text, bg=self.colors['bg'], fg=self.colors['fg'])

    def on_key_press(self, key):
        """Handle key press events."""
        self.update_lock_status()

    @staticmethod
    def get_capslock_status():
        """Check the status of Caps Lock."""
        return ctypes.windll.user32.GetKeyState(0x14) & 0x0001

    @staticmethod
    def get_numlock_status():
        """Check the status of Num Lock."""
        return ctypes.windll.user32.GetKeyState(0x90) & 0x0001

    def start_move(self, event):
        """Start dragging the window."""
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        """Perform the dragging of the window."""
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def open_settings(self):
        """Open the settings panel."""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("300x150")
        settings_window.configure(bg=self.colors['bg'])

        # Theme selection
        theme_label = tk.Label(settings_window, text="Select Theme:", bg=self.colors['bg'], fg=self.colors['fg'])
        theme_label.pack(pady=10)

        theme_var = tk.StringVar(value=self.theme)
        themes = ["light", "dark", "blue"]

        for theme in themes:
            tk.Radiobutton(
                settings_window, text=theme.capitalize(), variable=theme_var, value=theme,
                command=lambda: self.set_theme(theme_var.get()), bg=self.colors['bg'], fg=self.colors['fg'], selectcolor=self.colors['bg']
            ).pack(anchor=tk.W)

        # Auto-start setting
        start_var = tk.BooleanVar(value=self.auto_start)
        start_check = tk.Checkbutton(
            settings_window, text="Start with Windows", variable=start_var,
            command=lambda: self.toggle_auto_start(start_var.get()), bg=self.colors['bg'], fg=self.colors['fg'], selectcolor=self.colors['bg']
        )
        start_check.pack(anchor=tk.W, pady=5)

        # Close settings button
        close_button = tk.Button(settings_window, text="Close", command=settings_window.destroy, bg=self.colors['bg'], fg=self.colors['fg'])
        close_button.pack(pady=10)

    def set_theme(self, theme):
        """Set the theme and update colors."""
        self.theme = theme
        self.configure_theme()
        self.update_colors()

    def update_colors(self):
        """Update widget colors according to the theme."""
        self.root.configure(bg=self.colors["bg"])
        self.caps_label.configure(bg=self.colors["bg"], fg=self.colors["fg"])
        self.num_label.configure(bg=self.colors["bg"], fg=self.colors["fg"])

    def toggle_auto_start(self, value):
        """Toggle the auto-start setting."""
        self.auto_start = value
        messagebox.showinfo("Info", f"Auto-start {'enabled' if value else 'disabled'}!")

    def save_position(self):
        """Save the window position."""
        with open("position.txt", "w") as f:
            f.write(f"{self.root.winfo_x()},{self.root.winfo_y()}")

    def load_position(self):
        """Load the saved window position."""
        try:
            with open("position.txt", "r") as f:
                x, y = map(int, f.read().split(','))
                self.root.geometry(f"+{x}+{y}")
        except FileNotFoundError:
            pass

    def on_close(self):
        """Handle application closure."""
        self.save_position()
        self.root.destroy()

if __name__ == "__main__":
    LockIndicator()
