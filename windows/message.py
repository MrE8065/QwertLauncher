import customtkinter as ctk


def center_window_to_display(screen: ctk.CTkToplevel, width: int, height: int, scale_factor: float = 1.0):
  """Centers the window to the main display/monitor"""
  screen_width = screen.winfo_screenwidth()
  screen_height = screen.winfo_screenheight()
  x = int(((screen_width/2) - (width/2)) * scale_factor)
  y = int(((screen_height/2) - (height/1.5)) * scale_factor)
  return f"{width}x{height}+{x}+{y}"


def messagebox(master, title='Warning!', text='Placeholder', button_text='OK'):
  """Crear una ventana de diálogo"""

  message_box = ctk.CTkToplevel()
  message_box.geometry(center_window_to_display(master, 600, 150, message_box._get_window_scaling()))
  message_box.title(title)
  message_box.resizable(False, False)
  message_box.attributes('-topmost', True)
  message_box.grab_set()

  l1 = ctk.CTkLabel(message_box, text=text)
  l1.pack(pady=30)

  colored_frame = ctk.CTkFrame(message_box, height=1)
  colored_frame.pack(side="bottom", fill="x")

  b1 = ctk.CTkButton(colored_frame, text=button_text, command=message_box.destroy)
  b1.pack(pady=5)
