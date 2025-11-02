import customtkinter as ctk
import minecraft_launcher_lib as mll
from lib.minecraft import is_valid_version
import lib.variables as app_vars


def install_window(app):
  """Función para crear la ventana de instalaciones"""

  def center_window_to_display(screen: ctk.CTkToplevel, width: int, height: int, scale_factor: float = 1.0):
    """Centers the window to the main display/monitor"""
    screen_width = screen.winfo_screenwidth()
    screen_height = screen.winfo_screenheight()
    x = int(((screen_width/2) - (width/2)) * scale_factor)
    y = int(((screen_height/2) - (height/1.5)) * scale_factor)
    return f"{width}x{height}+{x}+{y}"

  def reset_info():
    status_label.configure(text="Selecciona una versión", text_color="white")

  def download_click():
    print(f"Options: {version_combobox.get()}, {selection_var.get()}")
    valid = is_valid_version(version_combobox.get(), selection_var.get())
    print(valid)

    if valid:
      print("Versión válida")
      reset_info()
      progress_bar.grid(row=4, column=0, columnspan=4, pady=(20, 0))
      progress_bar.start()
    else:
      print("Versión no válida")
      status_label.configure(text="Versión no válida", text_color="red")
      window.after(3000, reset_info)  # Resetear el texto después de 3 segundos

  window = ctk.CTkToplevel()
  window.title("Descargar")
  window.geometry(center_window_to_display(app, 600, 400, app._get_window_scaling()))
  window.resizable(False, False)
  window.transient(app)
  window.lift()
  window.focus()
  window.grab_set()

  # Crear un frame principal para contener todos los elementos
  main_frame = ctk.CTkFrame(window, fg_color="transparent")
  main_frame.place(relx=0.5, rely=0.5, anchor="center")

  status_label = ctk.CTkLabel(main_frame, text="Selecciona una versión", font=("Arial", 16))
  status_label.grid(row=0, column=0, columnspan=4, pady=(0, 10))

  versions = mll.utils.get_available_versions(app_vars.MINECRAFT_DIRECTORY)
  version_ids = [v["id"] for v in versions]
  version_combobox = ctk.CTkComboBox(main_frame, values=version_ids, width=250, height=50)
  version_combobox.grid(row=1, column=0, padx=(0, 10), pady=(0, 20), sticky="ew", columnspan=3)
  if version_ids:
    version_combobox.set(version_ids[0])

  def selection_changed(sel):
    selection_var.set(sel.lower())

  selection_var = ctk.StringVar(value="vanilla")

  selection_buttons = ctk.CTkSegmentedButton(main_frame, values=["Vanilla", "Fabric", "Forge", "Neoforge", "Quilt"], command=selection_changed)
  selection_buttons.grid(row=2, column=0, columnspan=4, padx=0, pady=(0, 20), sticky="ew")
  selection_buttons.set("Vanilla")

  install_button = ctk.CTkButton(main_frame, command=download_click, height=50, width=250, text="Descargar versión")
  install_button.grid(row=3, column=0, columnspan=4, pady=(0, 0))

  progress_bar = ctk.CTkProgressBar(main_frame, mode="indeterminate", height=15, width=125)
