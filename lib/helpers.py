from os import path
from tkinter import PhotoImage

import customtkinter as ctk

# https://github.com/TomSchimansky/CustomTkinter/discussions/1820


def center_window_to_display(screen: ctk.CTk | ctk.CTkToplevel, width: int, height: int, scale_factor: float = 1.0):
    """Centers the window to the main display/monitor"""
    screen_width = screen.winfo_screenwidth()
    screen_height = screen.winfo_screenheight()
    x = int(((screen_width/2) - (width/2)) * scale_factor)
    y = int(((screen_height/2) - (height/1.5)) * scale_factor)
    return f"{width}x{height}+{x}+{y}"


base_path = path.abspath(path.join(path.dirname(__file__), ".."))


def set_icon(window):
    """Establece el icono de la ventana"""
    icon_path = path.join(base_path, "assets", "icon.png")
    icon = PhotoImage(file=icon_path)
    window.wm_iconbitmap()
    window.after(300, lambda: window.iconphoto(False, icon))
