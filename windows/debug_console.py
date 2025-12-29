# Este script está hecho con IA. Se crees poder hacerlo mejor, haz un Pull Request :(

import re
import sys
from os import path
from tkinter import PhotoImage

import customtkinter as ctk

_orig_stdout = sys.stdout
_orig_stderr = sys.stderr
_redirector = None

# Mapeo simple de colores ANSI a hex
_ANSI_COLORS = {
    30: "#000000", 31: "#ff0000", 32: "#00aa00", 33: "#ffaa00",
    34: "#4040ff", 35: "#aa00ff", 36: "#00aaaa", 37: "#ffffff"
}

_ANSI_RE = re.compile(r'\x1b\[(?P<code>[0-9;]+)m')


class _ConsoleRedirector:
    def __init__(self, app):
        self.app = app
        self.window = ctk.CTkToplevel(app)
        self.window.title("Debug Console")
        self.window.geometry("700x300")
        # self.window.transient(app)
        self.window.lift()
        # self.window.grab_set()

        base_path = path.abspath(path.join(path.dirname(__file__), ".."))
        icon_path = path.join(base_path, "assets/icon.png")
        icon = PhotoImage(file=icon_path)
        self.window.wm_iconbitmap()
        self.window.after(300, lambda: self.window.iconphoto(False, icon))

        self.text = ctk.CTkTextbox(self.window, width=680, height=260)
        self.text.pack(fill="both", expand=True, padx=8, pady=8)

    def _ensure_tag(self, color_hex):
        """Crea/taggea un tag para color si no existe (nombre sin '#')."""
        if not color_hex:
            return None
        tag_name = f"ansi_fg_{color_hex.lstrip('#')}"
        if not getattr(self.text, "tag_names", lambda: ()) or tag_name not in self.text.tag_names():
            # Intenta ambos nombres de API: tag_config o tag_configure
            try:
                self.text.tag_config(tag_name, foreground=color_hex)
            except Exception:
                try:
                    self.text.tag_configure(tag_name, foreground=color_hex)
                except Exception:
                    # widget no soporta tags -> nada que hacer
                    return None
        return tag_name

    def _split_ansi(self, s):
        """Divide la cadena en segmentos (texto, color_hex) respetando códigos ANSI."""
        parts = []
        last = 0
        cur_color = None
        for m in _ANSI_RE.finditer(s):
            if m.start() > last:
                parts.append((s[last:m.start()], cur_color))
            codes = m.group("code").split(";")
            for c in codes:
                try:
                    val = int(c)
                except Exception:
                    continue
                if val == 0:
                    cur_color = None
                elif 30 <= val <= 37:
                    cur_color = _ANSI_COLORS.get(val)
            last = m.end()
        if last < len(s):
            parts.append((s[last:], cur_color))
        return parts

    def write(self, s):
        if not s:
            return

        def append():
            try:
                # Si no hay códigos ANSI rápidos, inserta directamente
                if "\x1b[" not in s:
                    try:
                        self.text.insert("end", s)
                        self.text.see("end")
                        return
                    except Exception:
                        pass

                # Si hay ANSI, parsea y aplica tags de color
                for chunk, color in self._split_ansi(s):
                    if not chunk:
                        continue
                    tag = self._ensure_tag(color)
                    try:
                        if tag:
                            self.text.insert("end", chunk, tag)
                        else:
                            self.text.insert("end", chunk)
                        self.text.see("end")
                    except Exception:
                        # Si insertar con tags falla, intenta insertar sin ellos
                        try:
                            self.text.insert("end", chunk)
                        except Exception:
                            pass
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
