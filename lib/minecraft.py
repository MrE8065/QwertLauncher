import json
import subprocess
import uuid

import minecraft_launcher_lib as mll
from minecraft_launcher_lib.types import CallbackDict, MinecraftOptions

import lib.variables as app_vars


def get_configs():
  """Obtener las configuraciones en el archivo config.json"""

  try:
    # Obtener la ruta del archivo config
    file = app_vars.CONFIG_JSON

    # Leer y parsear el archivo JSON
    with open(file, 'r', encoding='utf-8') as file:
      config = json.load(file)

    # Obtener los valores
    nombre = config.get('Nombre', '')
    ram = config.get('RAM', '')

    return nombre, ram

  except FileNotFoundError:
    print("Archivo config no encontrado")
    return "", ""
  except json.JSONDecodeError:
    print("Error leyendo el archivo JSON")
    return "Error", "Error"


def save_configs(nombre: str, ram: int):
  """Guardar las configuraciones en el archivo config.json"""

  # Obtener la ruta del archivo config
  file = app_vars.CONFIG_JSON

  # Crear el diccionario de configuraciones
  config = {
      'Nombre': nombre,
      'RAM': ram
  }

  # Escribir el archivo JSON
  with open(file, 'w', encoding='utf-8') as file:
    json.dump(config, file, indent=4)


def install_version(version: str, release_type: str, callback: CallbackDict):
  """
  Instala la versión especificada

  Args:
    version: Versión a instalar
    release_type: Tipo de versión (vanilla, fabric, forge, neoforge, quilt)
    callback: Diccionario con callbacks para progreso (setStatus, setProgress, setMax)

  Returns:
    Tupla (success: bool, error_msg: str or None)
  """
  try:
    if release_type == "vanilla":
      mll.install.install_minecraft_version(version, app_vars.MINECRAFT_DIRECTORY, callback=callback)
    else:
      loader = mll.mod_loader.get_mod_loader(release_type)
      loader.install(version, app_vars.MINECRAFT_DIRECTORY, callback=callback)

    return True, None

  except Exception as e:
    return False, str(e)


async def play_mine(version):
  """Llama al proceso de inicio del juego"""

  with open(app_vars.CONFIG_JSON, 'r', encoding='utf-8') as file:
    data = json.load(file)

  mine_user = data.get('Nombre', 'Player')
  ram = data.get('RAM', 2)

  options: MinecraftOptions = {
      'username': mine_user,
      'uuid': str(uuid.uuid4()),  # Durante las pruebas, descubrí que neoforge necesita si o si una uuid. Los demás funcionan sin una
      'token': '',
      "jvmArguments": [f"-Xmx{ram}G", f"-Xms{ram}G"],
  }

  subprocess.run(mll.command.get_minecraft_command(version, app_vars.MINECRAFT_DIRECTORY, options), check=True)


def is_valid_version(version: str, release_type: str):
  """Comprueba si la versión especificada existe (tanto en vanilla como en mod loaders)"""

  if release_type == "vanilla":
    valid = mll.utils.is_version_valid(version, app_vars.MINECRAFT_DIRECTORY)
    return valid
  else:
    valid = mll.mod_loader.get_mod_loader(release_type).is_minecraft_version_supported(version)
    return valid
