import os
import json
import time
import subprocess
import minecraft_launcher_lib as mll
from minecraft_launcher_lib.types import MinecraftOptions

from .variables import *

def get_configs():
  try:
    # Obtener la ruta del archivo config
    file = os.path.join(mll.utils.get_minecraft_directory(), 'config.json')
    
    # Leer y parsear el archivo JSON
    with open(file, 'r') as file:
      config = json.load(file)
      
    # Obtener los valores
    nombre = config.get('Nombre', '')
    ram = config.get('RAM', '')
    
    return nombre, ram
    
  except FileNotFoundError:
    print("Archivo config no encontrado")
    return None, None
  except json.JSONDecodeError:
    print("Error leyendo el archivo JSON")
    return None, None

async def install_minecraft(menu_func):
    global downloading
    os.system('cls')
    print("Selecciona la versión que quieres instalar (o escribe 0 para volver):")
    minecraft_version = input('» ')
    
    if minecraft_version == "0":
        await menu_func()
        return
    
    if mll.utils.is_version_valid(minecraft_version, MINECRAFT_DIRECTORY):
        os.system('cls')
        mll.install.install_minecraft_version(minecraft_version, MINECRAFT_DIRECTORY, callback=callback)
        downloading = False
        time.sleep(0.2)  # Para evitar solapamiento de textos
        print(f"\n» Versión {minecraft_version} instalada correctamente")
        time.sleep(1.5)
        await menu_func()
    else:
        downloading = False
        print(f"\nERROR: {minecraft_version} no es una versión válida")
        time.sleep(1.5)
        await install_minecraft(menu_func)

async def install_forge(menu_func):
    global downloading
    os.system('cls')
    print('Introduce la versión de Minecraft con Forge (o pulsa Enter para volver):')
    forge_ver = input('» ')
    
    if forge_ver == "":
        await menu_func()
        return
    
    try:
        forge = mll.forge.find_forge_version(forge_ver)
        mll.forge.install_forge_version(forge, MINECRAFT_DIRECTORY, callback=callback)
        downloading = False
        time.sleep(0.2)
        print("\n◈ Forge instalado correctamente ◈")
        time.sleep(1.5)
        await menu_func()
    except Exception as e:
        downloading = False
        print(f"\nERROR: Versión no válida - {str(e)}")
        time.sleep(10)
        await install_forge(menu_func)

async def install_fabric(menu_func):
    global downloading
    os.system('cls')
    print('Introduce la versión de Minecraft con Fabric (o escribe 0 para volver):')
    fabric_ver = input('» ')
    
    if fabric_ver == "0":
        await menu_func()
        return
    
    if mll.fabric.is_minecraft_version_supported(fabric_ver):
        mll.fabric.install_fabric(fabric_ver, MINECRAFT_DIRECTORY, callback=callback)
        downloading = False
        time.sleep(0.2)
        print("\n◈ Fabric instalado correctamente ◈")
        time.sleep(1.5)
        await menu_func()
    else:
        downloading = False
        print("\nERROR: Versión no soportada por Fabric")
        time.sleep(2)
        await install_fabric(menu_func)

async def play_mine(version):
  with open(CONFIG_JSON, 'r') as file:
    data = json.load(file)
    
  mine_user = data.get('Nombre', 'Player')
  ram = data.get('RAM', 2)

  options: MinecraftOptions = {
    'username': mine_user,
    'uuid': '',
    'token': '',
    "jvmArguments": [f"-Xmx{ram}G", f"-Xms{ram}G"],
  }
  
  subprocess.run(mll.command.get_minecraft_command(version, MINECRAFT_DIRECTORY, options))

def is_valid_version(version: str, type: str):
  if (type == "vanilla"):
    valid = mll.utils.is_version_valid(version, mll.utils.get_minecraft_directory())
    return valid
  else:
    valid = mll.mod_loader.get_mod_loader(type).is_minecraft_version_supported(version)
    return valid