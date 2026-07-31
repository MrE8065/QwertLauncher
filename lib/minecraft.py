import json
import subprocess
import uuid

import minecraft_launcher_lib as mll
from minecraft_launcher_lib.types import CallbackDict, MinecraftOptions

from lib.variables import CONFIG_JSON, MINECRAFT_DIRECTORY


def get_config_data():
    """Leer el contenido del archivo config.json si existe."""

    try:
        with open(CONFIG_JSON, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}


def get_configs():
    """Obtener las configuraciones en el archivo config.json"""

    config = get_config_data()
    nombre = config.get('Nombre', '')
    ram = config.get('RAM', '')

    return nombre, ram


def get_last_version():
    """Obtener la última versión seleccionada desde el archivo de configuración."""

    config = get_config_data()
    return config.get('lastVersion', '')


def save_configs(nombre: str, ram: int, last_version: str | None = None):
    """Guardar las configuraciones en el archivo config.json"""

    file = CONFIG_JSON
    config = get_config_data()

    config['Nombre'] = nombre
    config['RAM'] = ram
    if last_version is not None:
        config['lastVersion'] = last_version

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
            mll.install.install_minecraft_version(version, MINECRAFT_DIRECTORY, callback=callback)
        else:
            loader = mll.mod_loader.get_mod_loader(release_type)
            loader.install(version, MINECRAFT_DIRECTORY, callback=callback)

        return True, None

    except Exception as e:
        return False, str(e)


async def play_mine(version, game_dir: str | None = None):
    """Llama al proceso de inicio del juego"""

    with open(CONFIG_JSON, 'r', encoding='utf-8') as file:
        data = json.load(file)

    mine_user = data.get('Nombre', 'Player')
    ram = data.get('RAM', 2)

    options: MinecraftOptions = {
        'username': mine_user,
        'uuid': str(uuid.uuid4()),  # Durante las pruebas, descubrí que neoforge necesita si o si una uuid. Los demás funcionan sin una
        'token': '',
        "jvmArguments": [f"-Xmx{ram}G", f"-Xms{ram}G"],
    }

    if game_dir:
        options["gameDirectory"] = game_dir

    subprocess.run(mll.command.get_minecraft_command(version, MINECRAFT_DIRECTORY, options), check=True)


def is_valid_version(version: str, release_type: str):
    """Comprueba si la versión especificada existe (tanto en vanilla como en mod loaders)"""

    if release_type == "vanilla":
        valid = mll.utils.is_version_valid(version, MINECRAFT_DIRECTORY)
        return valid
    else:
        valid = mll.mod_loader.get_mod_loader(release_type).is_minecraft_version_supported(version)
        return valid
