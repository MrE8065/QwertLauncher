import sys
import customtkinter as ctk

_orig_stdout = sys.stdout
_orig_stderr = sys.stderr
_redirector = None


class _ConsoleRedirector:
  def __init__(self, app):
    self.app = app
    self.window = ctk.CTkToplevel(app)
    self.window.title("Debug Console")
    self.window.geometry("700x300")
    # self.window.transient(app)
    self.window.lift()
    # self.window.grab_set()
    try:
      self.text = ctk.CTkTextbox(self.window, width=680, height=260)
      self.text.pack(fill="both", expand=True, padx=8, pady=8)
    except Exception:
      # Fallback to classic tkinter.Text if CTkTextbox no está disponible
      import tkinter as tk
      self.text = tk.Text(self.window)
      self.text.pack(fill="both", expand=True, padx=8, pady=8)

  def write(self, s):
    if not s:
      return

    def append():
      try:
        self.text.insert("end", s)
        self.text.see("end")
      except Exception:
        pass
    try:
      self.app.after(0, append)
    except Exception:
      append()

  def flush(self):
    return


def attach_to_app(app):
  global _redirector
  if _redirector:
    return
  _redirector = _ConsoleRedirector(app)
  sys.stdout = _redirector
  sys.stderr = _redirector


def detach():
  global _redirector
  if not _redirector:
    return
  sys.stdout = _orig_stdout
  sys.stderr = _orig_stderr
  try:
    _redirector.window.destroy()
  except Exception:
    pass
  _redirector = None
