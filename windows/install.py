import customtkinter as ctk
from PIL import Image
import minecraft_launcher_lib as mll

def InstallWindow(app):
  def CenterWindowToDisplay(Screen: ctk.CTkToplevel, width: int, height: int, scale_factor: float = 1.0):
    """Centers the window to the main display/monitor"""
    screen_width = Screen.winfo_screenwidth()
    screen_height = Screen.winfo_screenheight()
    x = int(((screen_width/2) - (width/2)) * scale_factor)
    y = int(((screen_height/2) - (height/1.5)) * scale_factor)
    return f"{width}x{height}+{x}+{y}"

  def search_click():
    if (selection_var.get() == "forge"):
      forge = mll.forge.find_forge_version(version_combobox.get())
      print(forge)
    elif (selection_var.get() == "fabric"):
      fabric = mll.fabric.is_minecraft_version_supported(version_combobox.get())
      print(fabric)
    else:
      print("Vanilla")
    
  def download_click():
    print("Descargar versión")

  window = ctk.CTkToplevel()
  window.title("Descargar")
  window.geometry(CenterWindowToDisplay(app, 600, 400, app._get_window_scaling()))
  window.resizable(False,False)
  window.transient(app)
  window.lift()
  window.focus()
  window.grab_set()
  window.wm_iconbitmap(bitmap="assets/icon.ico")
  
  # Crear un frame principal para contener todos los elementos
  main_frame = ctk.CTkFrame(window, fg_color="transparent")
  main_frame.place(relx=0.5, rely=0.5, anchor="center")
  
  versions = mll.utils.get_available_versions(mll.utils.get_minecraft_directory())
  version_ids = [v["id"] for v in versions]
  version_combobox = ctk.CTkComboBox(main_frame, values=version_ids, width=250, height=50)
  version_combobox.grid(row=0, column=0, padx=20, pady=(0, 20), sticky="ew", columnspan=2)
  if version_ids:
    version_combobox.set(version_ids[0])
  
  search_image = ctk.CTkImage(Image.open("assets/search.png"), size=(50, 50))
  search_button = ctk.CTkButton(main_frame, command=search_click, height=50, width=50, font=("Arial", 30), image=search_image, text="")
  search_button.grid(row=0, column=2, padx=20, pady=(0, 20), sticky="w", columnspan=3)
  
  #checkbox_fabric = ctk.CTkCheckBox(main_frame, text="Fabric")
  #checkbox_fabric.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")
  
  selection_var = ctk.StringVar(value="none")
  
  selection_vanilla = ctk.CTkRadioButton(main_frame, text="Vanilla", variable=selection_var, value="vanilla")
  selection_vanilla.grid(row=1, column=0, padx=10, pady=(0, 20), sticky="ew") 
  selection_vanilla.select()
  
  selection_fabric = ctk.CTkRadioButton(main_frame, text="Fabric", variable=selection_var, value="fabric")
  selection_fabric.grid(row=1, column=1, padx=10, pady=(0, 20), sticky="ew") 
  
  #checkbox_forge = ctk.CTkCheckBox(main_frame, text="Forge")
  #checkbox_forge.grid(row=1, column=1, padx=20, pady=(0, 20), sticky="w")
  
  selection_forge = ctk.CTkRadioButton(main_frame, text="Forge", variable=selection_var, value="forge")
  selection_forge.grid(row=1, column=2, padx=10, pady=(0, 20), sticky="ew")
  
  install_button = ctk.CTkButton(main_frame, command=download_click, height=50, width=100, text="Descargar versión")
  install_button.grid(row=2, column=0, columnspan=3, padx=20, pady=(0, 20))