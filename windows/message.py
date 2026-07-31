from os import path
from tkinter import PhotoImage

import customtkinter as ctk

from lib.helpers import center_window_to_display


def messagebox(master, title='Warning!', text='Placeholder', button_text='OK'):
    """Crear una ventana de diálogo"""

    message_box = ctk.CTkToplevel()
    message_box.geometry(center_window_to_display(master, 600, 150, message_box._get_window_scaling()))
    message_box.title(title)
    message_box.resizable(False, False)
    message_box.attributes('-topmost', True)
    message_box.grab_set()

    base_path = path.abspath(path.join(path.dirname(__file__), ".."))
    icon_path = path.join(base_path, "assets/icon.png")
    icon = PhotoImage(file=icon_path)
    message_box.wm_iconbitmap()
    message_box.after(300, lambda: message_box.iconphoto(False, icon))

    l1 = ctk.CTkLabel(message_box, text=text)
    l1.pack(pady=30)

    colored_frame = ctk.CTkFrame(message_box, height=1)
    colored_frame.pack(side="bottom", fill="x")

    b1 = ctk.CTkButton(colored_frame, text=button_text, command=message_box.destroy)
    b1.pack(pady=5)
