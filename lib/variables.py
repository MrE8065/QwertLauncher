import os
import minecraft_launcher_lib as mll

IS_TESTING = True
LAUNCHER_VERSION = '1.0'
if IS_TESTING:
  print("Modo de pruebas")
  MINECRAFT_DIRECTORY = mll.utils.get_minecraft_directory().replace(".minecraft", ".qwert-test")
  if not os.path.exists(MINECRAFT_DIRECTORY):
    os.mkdir(MINECRAFT_DIRECTORY)
  else:
    pass
else:
  MINECRAFT_DIRECTORY = mll.utils.get_minecraft_directory()
CONFIG_JSON = os.path.join(MINECRAFT_DIRECTORY, 'config.json')
