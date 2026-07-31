import customtkinter as ctk

from lib.helpers import set_icon


def error_window(app, content):
    """Crea una ventana mostrando el log del error al ejecutar"""

    window = ctk.CTkToplevel(app)
    window.title("Error")
    window.geometry("700x300")
    window.lift()

    set_icon(window)

    text = ctk.CTkTextbox(window, width=680, height=260)
    text.pack(fill="both", expand=True, padx=8, pady=8)
    text.insert("0.0", content)
