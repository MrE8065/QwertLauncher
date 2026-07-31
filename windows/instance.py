import json
from os import path
from tkinter import PhotoImage
import re

import customtkinter as ctk

import minecraft_launcher_lib as mll
from windows.message import messagebox

from lib.variables import MINECRAFT_DIRECTORY


def center_window_to_display(screen: ctk.CTkToplevel, width: int, height: int, scale_factor: float = 1.0):
    """Centers the window to the main display/monitor"""
    screen_width = screen.winfo_screenwidth()
    screen_height = screen.winfo_screenheight()
    x = int(((screen_width/2) - (width/2)) * scale_factor)
    y = int(((screen_height/2) - (height/1.5)) * scale_factor)
    return f"{width}x{height}+{x}+{y}"


def instance_window(app):
    """Crea la ventana de creación de instancias"""

    def create_click():
        name = name_entry.get().strip()
        version = version_combobox.get().strip()

        if not name:
            messagebox(main_frame, text="El nombre de instancia no puede estar vacío")
            return

        if not version:
            messagebox(main_frame, text="Versión no válida")
            return

        if any(loader in version for loader in ("neoforge", "forge", "fabric")):
            instance_type = "custom"
        else:
            # Detecta el tipo de versión de acuerdo a si contiene solo números y puntos o también texto
            if bool(re.fullmatch(r'\d+(\.\d+)*', version)):
                instance_type = "release"
            else:
                instance_type = "snapshot"

        profiles_path = path.join(MINECRAFT_DIRECTORY, "launcher_profiles.json")
        profiles_data = {"profiles": {}, "settings": {}, "version": 3}

        if path.exists(profiles_path):
            try:
                with open(profiles_path, "r", encoding="utf-8") as file:
                    profiles_data = json.load(file)
            except (json.JSONDecodeError, OSError):
                profiles_data = {"profiles": {}, "settings": {}, "version": 3}

        if not isinstance(profiles_data.get("profiles"), dict):
            profiles_data["profiles"] = {}
        if not isinstance(profiles_data.get("settings"), dict):
            profiles_data["settings"] = {}
        if "version" not in profiles_data:
            profiles_data["version"] = 3

        profiles_data["profiles"][name] = {
            "name": name,
            "type": instance_type,
            "lastVersionId": version,
            "gameDir": path.join(MINECRAFT_DIRECTORY, "instances", name),
        }

        with open(profiles_path, "w", encoding="utf-8") as file:
            json.dump(profiles_data, file, indent=2)
            file.write("\n")

        messagebox(main_frame, text="Nueva instancia creada con éxito")

    window = ctk.CTkToplevel()
    window.title("Instancias")
    window.geometry(center_window_to_display(app, 600, 400, app._get_window_scaling()))
    window.resizable(False, False)
    window.transient(app)
    window.lift()
    window.focus()
    window.grab_set()

    base_path = path.abspath(path.join(path.dirname(__file__), ".."))
    icon_path = path.join(base_path, "assets/icon.png")
    icon = PhotoImage(file=icon_path)
    window.wm_iconbitmap()
    window.after(300, lambda: window.iconphoto(False, icon))

    # -- Crear un frame principal para contener todos los elementos --
    main_frame = ctk.CTkFrame(window, fg_color="transparent")
    main_frame.place(relx=0.5, rely=0.5, anchor="center")

    # ----------------------------------------------------------------

    # -- Nombre de instancia --
    name_label = ctk.CTkLabel(main_frame, text="Nombre de instancia:", justify="left")
    name_label.grid(row=1, column=0, pady=(0, 10), padx=(0, 5))

    name_entry = ctk.CTkEntry(main_frame, width=150, height=30, placeholder_text="Nueva instancia")
    name_entry.grid(row=1, column=1, pady=(0, 10), sticky="ew")

    # --------------------------

    # -- Lista con las versiones instaladas --
    versions = mll.utils.get_installed_versions(MINECRAFT_DIRECTORY)
    version_ids = [v["id"] for v in versions]

    version_label = ctk.CTkLabel(main_frame, text="Versión:", justify="left")
    version_label.grid(row=3, column=0, pady=(0, 10), padx=(0, 5))

    version_combobox = ctk.CTkComboBox(main_frame, values=version_ids)
    version_combobox.grid(row=3, column=1, pady=(0, 10), sticky="ew")
    if not version_ids:
        version_combobox.set("Sin versiones")

    # -------------------------------------------

    # -- Botón de instalar --
    install_button = ctk.CTkButton(
        main_frame,
        height=50,
        width=250,
        text="Crear nueva instancia",
        command=create_click,
        state="disabled" if not version_ids else "normal",  # Deshabilitar el botón si no hay versiones instaladas
    )
    install_button.grid(row=5, column=0, columnspan=2)
