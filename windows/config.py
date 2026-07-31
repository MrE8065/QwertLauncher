import logging

import customtkinter as ctk

from lib.minecraft import get_configs, save_configs
from lib.helpers import center_window_to_display, set_icon


logger = logging.getLogger("qwertlauncher")


def config_window(app):
    """Función para crear la ventana de configuración"""

    window = ctk.CTkToplevel()
    window.title("Config")
    window.geometry(center_window_to_display(app, 600, 400, app._get_window_scaling()))
    window.resizable(False, False)
    window.transient(app)
    window.lift()
    window.focus()
    window.grab_set()

    set_icon(window)

    username, ram = get_configs()

    config_frame = ctk.CTkFrame(window, fg_color="transparent")
    config_frame.place(relx=0.5, rely=0.5, anchor="center")

    # RAM texto centrado
    username_text = ctk.CTkLabel(config_frame, text="Nombre de usuario:")
    username_text.pack(pady=(0, 10))

    username_input = ctk.CTkEntry(config_frame, placeholder_text="Nombre de usuario", width=250, height=50)

    username_input.insert(0, username)

    username_input.pack(pady=(0, 20))

    # RAM texto centrado
    ram_text = ctk.CTkLabel(config_frame, text="Cantidad de RAM (en GB):")
    ram_text.pack(pady=(0, 10))

    # RAM input centrado
    ram_input = ctk.CTkEntry(config_frame, placeholder_text="Cantidad de RAM", width=250, height=50)

    ram_input.insert(0, ram)

    ram_input.pack(pady=(0, 10))

    def save_button_click():
        """Qué hacer cuando el botón de guardado es pulsado"""

        logger.info("Configuración guardada")
        save_configs(nombre=username_input.get(), ram=int(ram_input.get()))
        window.destroy()

    save_button = ctk.CTkButton(config_frame, text="Guardar", command=save_button_click, height=30, width=120)
    save_button.pack(expand=True, pady=(20, 0))
