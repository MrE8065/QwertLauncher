from os import path
from tkinter import PhotoImage

import customtkinter as ctk


def error_window(app, content):
    """Crea una ventana mostrando el log del error al ejecutar"""

    window = ctk.CTkToplevel(app)
    window.title("Error")
    window.geometry("700x300")
    window.lift()

    base_path = path.abspath(path.join(path.dirname(__file__), ".."))
    icon_path = path.join(base_path, "assets/icon.png")
    icon = PhotoImage(file=icon_path)
    window.wm_iconbitmap()
    window.after(300, lambda: window.iconphoto(False, icon))

    text = ctk.CTkTextbox(window, width=680, height=260)
    text.pack(fill="both", expand=True, padx=8, pady=8)
    text.insert("0.0", content)
