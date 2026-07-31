import threading
import logging

import customtkinter as ctk
import minecraft_launcher_lib as mll
from minecraft_launcher_lib.types import CallbackDict

from windows.message import messagebox

from lib.minecraft import install_version, is_valid_version
from lib.helpers import center_window_to_display, set_icon


logger = logging.getLogger("qwertlauncher")


def install_window(app):
    """Función para crear la ventana de instalaciones"""

    def reset_info():
        status_label.configure(text="Selecciona una versión", text_color="white")

    def set_status(text):
        """Actualiza el texto de estado"""
        logger.info(text)

    def set_progress(value):
        """Actualiza el valor de la barra de progreso"""
        if max_value[0] > 0:
            progress = value / max_value[0]
            window.after(0, lambda: progress_bar.set(progress))

    def set_max(value):
        """Establece el valor máximo de la barra de progreso"""
        max_value[0] = value

    def on_download_complete(success, error_msg=None):
        """Callback cuando termina la descarga"""
        if success:
            window.after(0, lambda: messagebox(main_frame, title="Éxito", text="Instalación completada con éxito"))
            window.after(0, lambda: progress_bar.set(1.0))
        else:
            window.after(0, lambda: messagebox(main_frame, title="Error", text=f"Error: {error_msg}"))
        window.after(0, lambda: progress_bar.grid_remove())

        window.after(0, lambda: install_button.configure(state="normal", text="Descargar versión"))

    def download_thread():
        """Hilo para descargar la versión sin bloquear la UI"""
        version = version_combobox.get()
        release_type = selection_var.get()

        # Llamar a la función de instalación en minecraft.py
        success, error = install_version(version, release_type, callback)
        on_download_complete(success, error)

    def download_click():
        version = version_combobox.get()
        release_type = selection_var.get()

        valid = is_valid_version(version, release_type)

        if valid:
            # Resetear valores
            max_value[0] = 0

            # Mostrar barra de progreso
            progress_bar.set(0)
            progress_bar.grid(row=4, column=0, columnspan=4, pady=(20, 0))

            # Deshabilitar botón durante descarga
            install_button.configure(state="disabled", text="Descargando...")

            # Iniciar descarga en un hilo separado
            thread = threading.Thread(target=download_thread, daemon=True)
            thread.start()
        else:
            status_label.configure(text="Versión no válida", text_color="red")
            window.after(3000, reset_info)

    # Variable para almacenar el máximo valor de progreso
    max_value = [0]

    # Crear el callback para la instalación
    callback: CallbackDict = {
        "setStatus": set_status,
        "setProgress": set_progress,
        "setMax": set_max
    }

    window = ctk.CTkToplevel()
    window.title("Descargar")
    window.geometry(center_window_to_display(app, 600, 400, app._get_window_scaling()))
    window.resizable(False, False)
    window.transient(app)
    window.lift()
    window.focus()
    window.grab_set()

    set_icon(window)

    # Crear un frame principal para contener todos los elementos
    main_frame = ctk.CTkFrame(window, fg_color="transparent")
    main_frame.place(relx=0.5, rely=0.5, anchor="center")

    status_label = ctk.CTkLabel(main_frame, text="Selecciona una versión", font=("Arial", 16))
    status_label.grid(row=0, column=0, columnspan=4, pady=(0, 10))

    versions = mll.utils.get_version_list()
    version_ids = [v["id"] for v in versions]

    version_combobox = ctk.CTkComboBox(main_frame, values=version_ids, width=250, height=50)
    version_combobox.grid(row=1, column=0, padx=(0, 10), pady=(0, 20), sticky="ew", columnspan=3)

    def selection_changed(sel):
        selection_var.set(sel.lower())

    selection_var = ctk.StringVar(value="vanilla")

    selection_buttons = ctk.CTkSegmentedButton(main_frame, values=["Vanilla", "Fabric", "Forge", "Neoforge", "Quilt"], command=selection_changed)
    selection_buttons.grid(row=2, column=0, columnspan=4, padx=0, pady=(0, 20), sticky="ew")
    selection_buttons.set("Vanilla")

    install_button = ctk.CTkButton(main_frame, command=download_click, height=50, width=250, text="Descargar versión")
    install_button.grid(row=3, column=0, columnspan=4, pady=(0, 0))

    progress_bar = ctk.CTkProgressBar(main_frame, mode="determinate", height=15, width=125)
