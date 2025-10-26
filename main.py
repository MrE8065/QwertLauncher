import customtkinter as ctk
from PIL import Image
from windows.config import ConfigWindow
from windows.install import InstallWindow
from lib.minecraft import get_configs, play_mine

import minecraft_launcher_lib as mll


def CenterWindowToDisplay(Screen: ctk.CTk, width: int, height: int, scale_factor: float = 1.0):
  """Centers the window to the main display/monitor"""
  screen_width = Screen.winfo_screenwidth()
  screen_height = Screen.winfo_screenheight()
  x = int(((screen_width/2) - (width/2)) * scale_factor)
  y = int(((screen_height/2) - (height/1.5)) * scale_factor)
  return f"{width}x{height}+{x}+{y}"


app = ctk.CTk()
app.title("QwertLauncher")
app.resizable(False, False)
app.geometry(CenterWindowToDisplay(app, 600, 300, app._get_window_scaling()))

username, _ = get_configs()


async def play_button_click():
  await play_mine(version_combobox.get())

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

versions = mll.utils.get_installed_versions(mll.utils.get_minecraft_directory())
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

def config_button_click():
  ConfigWindow(app)
  
config_image = ctk.CTkImage(Image.open("assets/settings_big.png"), size=(70, 70))
config_button = ctk.CTkButton(options_frame, text="", image=config_image, anchor="center", command=config_button_click, height=100, width=100)
config_button.pack(side="left", padx=10, pady=10)

username_text = ctk.CTkLabel(options_frame, text=f"Jugando como: {username}", font=("Arial", 20))
username_text.pack(side="left", expand=True)

def install_button_click():
  InstallWindow(app)

install_image = ctk.CTkImage(Image.open("assets/download_big.png"), size=(70, 70))
install_button = ctk.CTkButton(options_frame, text="", image=install_image, anchor="center", command=install_button_click, height=100, width=100)
install_button.pack(side="right", padx=10, pady=10)


app.mainloop()