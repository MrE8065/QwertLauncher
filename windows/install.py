import customtkinter as ctk
from PIL import Image
import minecraft_launcher_lib as mll
from lib.minecraft import is_valid_version

def InstallWindow(app):
  def CenterWindowToDisplay(Screen: ctk.CTkToplevel, width: int, height: int, scale_factor: float = 1.0):
    """Centers the window to the main display/monitor"""
    screen_width = Screen.winfo_screenwidth()
    screen_height = Screen.winfo_screenheight()
    x = int(((screen_width/2) - (width/2)) * scale_factor)
    y = int(((screen_height/2) - (height/1.5)) * scale_factor)
    return f"{width}x{height}+{x}+{y}"

  def search_click():
    print(f"Options: {version_combobox.get()}, {selection_var.get()}")
    test = is_valid_version(version_combobox.get(), selection_var.get())
    print(test)
    
    if test:
      status_label.configure(text="Versión válida", text_color="green")
      install_button.configure(state="normal")
    else:
      status_label.configure(text="Versión no válida", text_color="red")
      install_button.configure(state="disabled")
    
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
  
  # Crear un frame principal para contener todos los elementos
  main_frame = ctk.CTkFrame(window, fg_color="transparent")
  main_frame.place(relx=0.5, rely=0.5, anchor="center")
  
  status_label = ctk.CTkLabel(main_frame, text="Selecciona una versión", font=("Arial", 16))
  status_label.grid(row=0, column=0, columnspan=5, pady=(0, 10))
  
  versions = mll.utils.get_available_versions(mll.utils.get_minecraft_directory())
  version_ids = [v["id"] for v in versions]
  version_combobox = ctk.CTkComboBox(main_frame, values=version_ids, width=250, height=50)
  version_combobox.grid(row=1, column=0, padx=(0, 10), pady=(0, 20), sticky="ew", columnspan=4)
  if version_ids:
    version_combobox.set(version_ids[0])
  
  search_image = ctk.CTkImage(Image.open("assets/search.png"), size=(50, 50))
  search_button = ctk.CTkButton(main_frame, command=search_click, height=50, width=50, font=("Arial", 30), image=search_image, text="")
  search_button.grid(row=1, column=4, padx=(10, 0), pady=(0, 20))
  
  def selection_changed(sel):
    install_button.configure(state="disabled")
    selection_var.set(sel.lower())

  selection_var = ctk.StringVar(value="vanilla")
  
  selection_buttons = ctk.CTkSegmentedButton(main_frame, values=["Vanilla", "Fabric", "Forge", "Neoforge", "Quilt"], command=selection_changed)
  selection_buttons.grid(row=2, column=0, columnspan=5, padx=0, pady=(0, 20), sticky="ew")
  selection_buttons.set("Vanilla")
  
  install_button = ctk.CTkButton(main_frame, command=download_click, height=50, width=250, text="Descargar versión")
  install_button.grid(row=3, column=0, columnspan=5, pady=(0, 0))