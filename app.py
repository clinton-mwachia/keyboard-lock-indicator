import tkinter as tk
from pynput import keyboard
import ctypes
import json
import os
import threading
import pystray
from PIL import Image, ImageDraw

SETTINGS_FILE = "settings.json"


class LockIndicator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Lock Indicator")

        # Make window always on top
        self.root.attributes('-topmost', True)

        self.x = 0
        self.y = 0

        self.tray_icon = None

        # Defaults
        self.theme = "dark"
        self.auto_start = False
        self.position = (100, 100)

        self.load_settings()
        self.configure_theme()

        self.root.geometry(f"+{self.position[0]}+{self.position[1]}")
        self.root.configure(bg=self.colors["bg"])

        # Dragging
        self.root.bind("<ButtonPress-1>", self.start_move)
        self.root.bind("<B1-Motion>", self.do_move)

        # Frame
        self.frame = tk.Frame(self.root, bg=self.colors["bg"], padx=10, pady=5)
        self.frame.pack()

        self.caps_label = tk.Label(self.frame, font=("Segoe UI", 12, "bold"))
        self.caps_label.pack()

        self.num_label = tk.Label(self.frame, font=("Segoe UI", 10))
        self.num_label.pack()

        self.menu_button = tk.Button(
            self.frame, text="⚙", command=self.open_settings,
            bg=self.colors["bg"], fg=self.colors["fg"], relief="flat"
        )
        self.menu_button.pack(pady=2)

        self.update_lock_status()

        # Thread-safe listener
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        threading.Thread(target=self.setup_tray, daemon=True).start()

        self.root.mainloop()

    # ---------------- SETTINGS ---------------- #

    def save_settings(self):
        data = {
            "theme": self.theme,
            "position": (self.root.winfo_x(), self.root.winfo_y())
        }
        with open(SETTINGS_FILE, "w") as f:
            json.dump(data, f)

    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as f:
                data = json.load(f)
                self.theme = data.get("theme", "dark")
                self.position = tuple(data.get("position", (100, 100)))

    # ---------------- THEME ---------------- #

    def configure_theme(self):
        themes = {
            "light": {"bg": "#eeeeee", "fg": "#000000"},
            "dark": {"bg": "#1e1e1e", "fg": "#ffffff"},
            "blue": {"bg": "#005f73", "fg": "#ffffff"},
        }
        self.colors = themes[self.theme]

    def update_colors(self):
        self.root.configure(bg=self.colors["bg"])
        self.frame.configure(bg=self.colors["bg"])
        self.caps_label.configure(bg=self.colors["bg"], fg=self.colors["fg"])
        self.num_label.configure(bg=self.colors["bg"], fg=self.colors["fg"])
        self.menu_button.configure(bg=self.colors["bg"], fg=self.colors["fg"])

    # ---------------- LOCK STATUS ---------------- #

    def update_lock_status(self):
        caps = self.get_capslock_status()
        num = self.get_numlock_status()

        self.caps_label.config(text=f"Caps Lock {'ON' if caps else 'OFF'}")
        self.num_label.config(text=f"Num Lock {'ON' if num else 'OFF'}")

    def on_key_press(self, key):
        self.root.after(0, self.update_lock_status)

    @staticmethod
    def get_capslock_status():
        return ctypes.windll.user32.GetKeyState(0x14) & 1

    @staticmethod
    def get_numlock_status():
        return ctypes.windll.user32.GetKeyState(0x90) & 1

    # ---------------- DRAG ---------------- #

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        x = self.root.winfo_x() + (event.x - self.x)
        y = self.root.winfo_y() + (event.y - self.y)
        self.root.geometry(f"+{x}+{y}")

    # ---------------- SETTINGS WINDOW ---------------- #

    def open_settings(self):
        win = tk.Toplevel(self.root)
        win.title("Settings")
        win.geometry("220x160")
        win.configure(bg=self.colors["bg"])

        tk.Label(win, text="Theme:", bg=self.colors["bg"], fg=self.colors["fg"]).pack(pady=5)

        theme_var = tk.StringVar(value=self.theme)

        for t in ["light", "dark", "blue"]:
            tk.Radiobutton(
                win, text=t.capitalize(), variable=theme_var, value=t,
                bg=self.colors["bg"], fg=self.colors["fg"], selectcolor=self.colors["bg"],
                command=lambda: self.set_theme(theme_var.get())
            ).pack(anchor="w")

        tk.Button(win, text="Close", command=win.destroy).pack(pady=10)

    def set_theme(self, theme):
        self.theme = theme
        self.configure_theme()
        self.update_colors()

    # ---------------- TRAY ICON ---------------- #

    def setup_tray(self):
        image = self.create_image()
        menu = pystray.Menu(
            pystray.MenuItem("Show", self.show_window),
            pystray.MenuItem("Hide", self.hide_window),
            pystray.MenuItem("Quit", self.quit_app)
        )
        self.tray_icon = pystray.Icon("LockIndicator", image, "Lock Indicator", menu)
        self.tray_icon.run()

    def create_image(self):
        img = Image.new("RGB", (64, 64), "black")
        draw = ImageDraw.Draw(img)
        draw.rectangle((16, 16, 48, 48), fill="white")
        return img

    def hide_window(self):
        self.root.withdraw()

    def show_window(self):
        self.root.deiconify()

    def quit_app(self):
        self.tray_icon.stop()
        self.on_close()

    # ---------------- EXIT ---------------- #

    def on_close(self):
        try:
            self.save_settings()
            if self.tray_icon:
                self.tray_icon.stop()
        except:
            pass
        self.root.destroy()
        os._exit(0)



if __name__ == "__main__":
    try:
        LockIndicator()
    except KeyboardInterrupt:
        print("Exiting Lock Indicator...")

