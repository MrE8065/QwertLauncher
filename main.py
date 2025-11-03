import asyncio
import minecraft_launcher_lib as mll


import customtkinter as ctk
from PIL import Image
from windows.config import config_window
from windows.install import install_window
from windows.message import messagebox
from lib.minecraft import get_configs, play_mine

import lib.variables as app_vars
from lib.logger import *


def center_window_to_display(screen: ctk.CTk, width: int, height: int, scale_factor: float = 1.0):
  """Centers the window to the main display/monitor"""
  screen_width = screen.winfo_screenwidth()
  screen_height = screen.winfo_screenheight()
  x = int(((screen_width/2) - (width/2)) * scale_factor)
  y = int(((screen_height/2) - (height/1.5)) * scale_factor)
  return f"{width}x{height}+{x}+{y}"


app = ctk.CTk()
app.title("QwertLauncher")
app.resizable(False, False)
app.geometry(center_window_to_display(app, 600, 300, app._get_window_scaling()))

# Si estamos en modo testing, abrir la consola de debug que captura los prints
if app_vars.IS_TESTING:
  try:
    from lib.debug_console import attach_to_app
    attach_to_app(app)
  except Exception as e:
    show_error(f"Error iniciando consola de debug: {e}")

username, ram = get_configs()
if not username and not ram:
  show_warn("No se encontraron configuraciones. Mostrando ventana de aviso...")
  messagebox(app, title="Error!", text="No se encontraron configuraciones para el usuario.\n"
             "Accede a la ventana de configuración para establecer un nombre de usuario y la RAM asignada.\n"
             "Cierra y vuelve a abrir el launcher para aplicar los cambios.")
else:
  show_success("Configuraciones encontradas")
  show_info(f"Usuario: {username}, RAM: {ram}GB")


def play_button_click():
  """Qué hacer cuando el boton de jugar es pulsado"""
  version = version_combobox.get()
  asyncio.run(play_mine(version))


play_button = ctk.CTkButton(
    app,
    text="Jugar",
    command=play_button_click,
    height=120,
    font=("Arial", 30)
)

play_button.pack(pady=10, fill="x", padx=10)

version_frame = ctk.CTkFrame(app, fg_color="transparent")
version_frame.pack(pady=10, padx=20, fill="x")
version_label = ctk.CTkLabel(version_frame, text="Versión para jugar:", font=("Arial", 15))
version_label.pack(side="left", padx=10)

versions = mll.utils.get_installed_versions(app_vars.MINECRAFT_DIRECTORY)
version_ids = [v["id"] for v in versions]
version_combobox = ctk.CTkOptionMenu(version_frame, values=version_ids)
version_combobox.pack(side="right", fill="x", expand=True, padx=10)
if version_ids:
  version_combobox.set(version_ids[0])
  play_button.configure(state="normal")
else:
  version_combobox.set("Sin versiones encontradas")
  play_button.configure(state="disabled")

options_frame = ctk.CTkFrame(app, fg_color="transparent")
options_frame.pack(pady=(0, 10), padx=10, fill="x")

config_image = ctk.CTkImage(Image.open("assets/settings_big.png"), size=(70, 70))
config_button = ctk.CTkButton(options_frame, text="", image=config_image, anchor="center", command=lambda: config_window(app), height=100, width=100)
config_button.pack(side="left", padx=10, pady=10)

username_text = ctk.CTkLabel(options_frame, text=f"Jugando como: {username}", font=("Arial", 20))
username_text.pack(side="left", expand=True)

install_image = ctk.CTkImage(Image.open("assets/download_big.png"), size=(70, 70))
install_button = ctk.CTkButton(options_frame, text="", image=install_image, anchor="center",
                               command=lambda: install_window(app), height=100, width=100)
install_button.pack(side="right", padx=10, pady=10)


app.mainloop()
