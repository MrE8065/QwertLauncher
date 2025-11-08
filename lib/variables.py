import os

import minecraft_launcher_lib as mll

IS_TESTING = False  # Variable para determinar si usar el modo debug
MINECRAFT_DIRECTORY = mll.utils.get_minecraft_directory()  # Ruta predeterminada de minecraft: "C:\Users\USUARIO\AppData\Roaming\.minecraft"
# Crear la carpeta si no existe
if not os.path.exists(MINECRAFT_DIRECTORY):
  os.mkdir(MINECRAFT_DIRECTORY)
CONFIG_JSON = os.path.join(MINECRAFT_DIRECTORY, 'config.json')  # Ruta del archivo de configuración
