# Este script está hecho con IA

import logging

import customtkinter as ctk

from lib.helpers import set_icon


class _ConsoleHandler(logging.Handler):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.window = ctk.CTkToplevel(app)
        self.window.title("Debug Console")
        self.window.geometry("700x300")
        self.window.lift()

        set_icon(self.window)

        self.text = ctk.CTkTextbox(self.window, width=680, height=260)
        self.text.pack(fill="both", expand=True, padx=8, pady=8)

        self.setFormatter(logging.Formatter('[%(levelname)s]: %(message)s'))

    def emit(self, record):
        message = self.format(record) + "\n"

        def append():
            try:
                self.text.insert("end", message)
                self.text.see("end")
            except Exception:
                pass

        try:
            self.app.after(0, append)
        except Exception:
            append()


def attach_to_app(app):
    logging.getLogger("qwertlauncher").addHandler(_ConsoleHandler(app))
