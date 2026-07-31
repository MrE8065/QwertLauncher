import argparse
import asyncio
import threading
from os import path
import json
import logging

import customtkinter as ctk
import minecraft_launcher_lib as mll
from PIL import Image

import lib.variables as app_vars
from lib.minecraft import get_configs, get_last_version, play_mine, save_configs
from lib.helpers import center_window_to_display, set_icon, base_path
from windows.config import config_window
from windows.error import error_window
from windows.install import install_window
from windows.instance import instance_window
from windows.message import messagebox

# Configura el logger de la app a DEBUG
logging.basicConfig(format='[%(levelname)s]: %(message)s')
logger = logging.getLogger("qwertlauncher")
logger.setLevel(logging.DEBUG)

# Crea el parseador de argumentos
parser = argparse.ArgumentParser(description="QwertLauncher - Un launcher de Minecraft simple")
parser.add_argument("--debug", action="store_true", help="Activar el modo debug")
args = parser.parse_args()

# Establece IS_TESTING de acuerdo al argumento --debug
app_vars.IS_TESTING = args.debug


app = ctk.CTk()
app.title("QwertLauncher")
app.resizable(False, False)
app.geometry(center_window_to_display(app, 600, 300, app._get_window_scaling()))

set_icon(app)

# Si estamos en modo testing, abrir la consola de debug que captura los prints
if app_vars.IS_TESTING:
    try:
        from windows.debug_console import attach_to_app

        attach_to_app(app)
        logger.info("Modo de pruebas activado")
    except Exception as e:
        logger.error("Error iniciando consola de debug: %s", e)

username, ram = get_configs()
if not username and not ram:
    logger.warning("No se encontraron configuraciones. Mostrando ventana de aviso...")
    messagebox(
        app,
        title="Error!",
        text="No se encontraron configuraciones para el usuario.\n"
        "Accede a la ventana de configuración para establecer un nombre de usuario y la RAM asignada.\n"
        "Cierra y vuelve a abrir el launcher para aplicar los cambios.",
    )
else:
    logger.info("Usuario: %s, RAM: %sGB", username, ram)


def _run_play(version: str, game_dir: str | None = None):
    """Ejecuta play_mine en un hilo separado"""
    try:
        asyncio.run(play_mine(version, game_dir=game_dir))
    except Exception as e:
        logger.error("Error lanzando Minecraft: %s", e)
        if not app_vars.IS_TESTING:
            # Mostrar ventana con el error al lanzar el juego (en caso de no usar el modo debug)
            error_window(app, e)
    finally:
        # Reactivar el botón desde el hilo principal
        app.after(0, lambda: play_button.configure(state="normal"))


def play_button_click():
    """Qué hacer cuando el boton de jugar es pulsado"""
    selected_option = version_combobox.get()
    selected_profile = instance_profiles.get(selected_option, {})
    selected_version = selected_profile.get("lastVersionId") or selected_option
    selected_game_dir = selected_profile.get("gameDir")

    save_configs(username, ram, last_version=selected_option)

    # Desactivar el botón mientras se lanza
    play_button.configure(state="disabled")
    t = threading.Thread(target=_run_play, args=(selected_version, selected_game_dir), daemon=True)
    t.start()


play_button = ctk.CTkButton(app, text="Jugar", command=play_button_click, height=120, font=("Arial", 30))

play_button.pack(pady=10, fill="x", padx=10)

version_frame = ctk.CTkFrame(app, fg_color="transparent")
version_frame.pack(pady=10, padx=20, fill="x")
version_label = ctk.CTkLabel(version_frame, text="Versión para jugar:", font=("Arial", 15))
version_label.pack(side="left", padx=10)

versions = mll.utils.get_installed_versions(app_vars.MINECRAFT_DIRECTORY)
version_ids = [v["id"] for v in versions]
instance_profiles = {}

profiles_path = path.join(app_vars.MINECRAFT_DIRECTORY, "launcher_profiles.json")
if path.exists(profiles_path):
    with open(profiles_path, "r", encoding="utf-8") as file:
        profiles_data = json.load(file)
        for profile in profiles_data.get("profiles", {}).values():
            profile_name = profile.get("name")
            if profile_name:
                instance_profiles[profile_name] = {
                    "lastVersionId": profile.get("lastVersionId"),
                    "gameDir": profile.get("gameDir"),
                }
                if profile_name not in version_ids:
                    version_ids.append(profile_name)

version_combobox = ctk.CTkOptionMenu(version_frame, values=version_ids)
version_combobox.pack(side="right", fill="x", expand=True, padx=10)
if version_ids:
    last_selected_version = get_last_version()
    if last_selected_version in version_ids:
        version_combobox.set(last_selected_version)
    else:
        version_combobox.set(version_ids[0])
    play_button.configure(state="normal")
else:
    version_combobox.set("Sin versiones encontradas")
    play_button.configure(state="disabled")

options_frame = ctk.CTkFrame(app, fg_color="transparent")
options_frame.pack(pady=(0, 10), padx=10, fill="x")

path_to_settings = path.join(base_path, "assets", "settings_big.png")
config_image = ctk.CTkImage(Image.open(path_to_settings), size=(70, 70))
config_button = ctk.CTkButton(options_frame, text="", image=config_image, anchor="center", command=lambda: config_window(app), height=50, width=50)
config_button.pack(side="right", padx=10, pady=10)

username_text = ctk.CTkLabel(options_frame, text=f"Jugando como: {username}", font=("Arial", 20))
username_text.pack(side="left", expand=True)

path_to_download = path.join(base_path, "assets", "download_big.png")
install_image = ctk.CTkImage(Image.open(path_to_download), size=(70, 70))
install_button = ctk.CTkButton(
    options_frame, text="", image=install_image, anchor="center", command=lambda: install_window(app), height=50, width=50
)
install_button.pack(side="right", padx=10, pady=10)

path_to_instance = path.join(base_path, "assets", "library_add_big.png")
instance_image = ctk.CTkImage(Image.open(path_to_instance), size=(70, 70))
instance_button = ctk.CTkButton(
    options_frame, text="", image=instance_image, anchor="center", command=lambda: instance_window(app), height=50, width=50
)
instance_button.pack(side="right", padx=10, pady=10)


app.mainloop()
