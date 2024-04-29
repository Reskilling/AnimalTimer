import ctypes
import sys
import tkinter as tk
from PIL import Image, ImageTk
from datetime import datetime, timedelta
import os

if hasattr(sys, 'frozen'):
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    ctypes.windll.kernel32.SetConsoleTitleW("DogTimer")

class AppConfig:
    BACKGROUND_IMAGE_PATH = "background.png"
    BOWL_IMAGE_PATH = "bowl.gif"
    FULLSCREEN_IMAGE_PATH_OPEN = "fullscreen_open.gif"
    FULLSCREEN_IMAGE_PATH_CLOSE = "fullscreen_close.gif"
    RESET_TIME_MORNING = (6, 0)
    RESET_TIME_EVENING = (16, 30)
    UPDATE_INTERVAL = 1000
    FONT_STYLE = ("Cooper Black", 24)
    TEXT_COLOR = "black"

class ImageLoader:
    @staticmethod
    def load_image(image_path):
        try:
            img = Image.open(image_path)
            img.photo = ImageTk.PhotoImage(img)
            return img.photo
        except IOError as e:
            print(f"Error loading image: {e}")
            return None

class TimerManager:
    def __init__(self, canvas, display_label, bowl_button, fullscreen_button, timer_label):
        self.canvas = canvas
        self.display_label = display_label
        self.bowl_button = bowl_button
        self.fullscreen_button = fullscreen_button
        self.timer_label = timer_label

    def start_timer(self):
        end_time = self.calculate_next_reset_time()
        self.update_timer(end_time)

    def update_timer(self, end_time):
        remaining_time = max(end_time - datetime.now(), timedelta(0))
        hours, remainder = divmod(remaining_time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.canvas.itemconfig(self.timer_label, text=f"{hours:02}:{minutes:02}:{seconds:02}")

        if remaining_time > timedelta(0):
            self.canvas.after(AppConfig.UPDATE_INTERVAL, lambda: self.update_timer(end_time))
        else:
            self.reset_timer_display()

    def reset_timer_display(self):
        self.canvas.itemconfig(self.timer_label, text="")
        self.canvas.itemconfig(self.bowl_button, state=tk.NORMAL)
        self.canvas.itemconfig(self.fullscreen_button, state=tk.HIDDEN)

    def calculate_next_reset_time(self):
        now = datetime.now()
        reset_time_morning = datetime(now.year, now.month, now.day, *AppConfig.RESET_TIME_MORNING)
        reset_time_evening = datetime(now.year, now.month, now.day, *AppConfig.RESET_TIME_EVENING)

        if now >= reset_time_evening:
            return reset_time_morning + timedelta(days=1)
        else:
            return reset_time_evening

class JakeTimerApp:
    def __init__(self, root):
        self.root = root
        self.load_images()  # Load images during initialization
        self.setup_gui()

    def setup_gui(self):
        self.root.title("DogTimer")

        self.canvas = tk.Canvas(self.root, width=800, height=480, highlightthickness=0)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image)

        self.display_label = self.create_text(200, 50, "Jake has not eaten. 😢", AppConfig.FONT_STYLE, AppConfig.TEXT_COLOR)
        self.bowl_button = self.create_image(100, 75, self.bowl_image, self.on_bowl_click)
        self.fullscreen_button = self.create_image(768, 0, self.fullscreen_open_image, self.on_fullscreen_click)
        self.timer_label = self.create_text(175, 100, "", AppConfig.FONT_STYLE, AppConfig.TEXT_COLOR)

        self.timer_manager = TimerManager(self.canvas, self.display_label, self.bowl_button, self.fullscreen_button,
                                          self.timer_label)

    def load_images(self):
        self.bg_image = ImageLoader.load_image(resource_path(AppConfig.BACKGROUND_IMAGE_PATH))
        self.bowl_image = ImageLoader.load_image(resource_path(AppConfig.BOWL_IMAGE_PATH))
        self.fullscreen_open_image = ImageLoader.load_image(resource_path(AppConfig.FULLSCREEN_IMAGE_PATH_OPEN))
        self.fullscreen_close_image = ImageLoader.load_image(resource_path(AppConfig.FULLSCREEN_IMAGE_PATH_CLOSE))

    def on_bowl_click(self, event):
        self.canvas.itemconfig(self.display_label, text="Jake has been fed! 😀")
        self.canvas.itemconfig(self.bowl_button, state=tk.HIDDEN)
        self.canvas.itemconfig(self.fullscreen_button, state=tk.NORMAL)
        self.timer_manager.start_timer()

    def on_fullscreen_click(self, event):
        self.root.attributes('-fullscreen', not self.root.attributes('-fullscreen'))
        img = self.fullscreen_close_image if self.root.attributes('-fullscreen') else self.fullscreen_open_image
        self.canvas.itemconfig(self.fullscreen_button, image=img)

    def create_text(self, x, y, text, font, fill):
        return self.canvas.create_text(x, y, text=text, font=font, fill=fill)

    def create_image(self, x, y, image, click_handler=None):
        image_widget = self.canvas.create_image(x, y, anchor=tk.NW, image=image)
        if click_handler:
            self.canvas.tag_bind(image_widget, "<Button-1>", click_handler)
        return image_widget

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = JakeTimerApp(root)
    root.mainloop()
