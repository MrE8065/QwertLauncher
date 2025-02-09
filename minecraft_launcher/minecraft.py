import os
import json
import time
import subprocess
import minecraft_launcher_lib
import itertools
import sys

from .variables import *

# Configuración del spinner
spinner_chars = itertools.cycle(['|', '/', '-', '\\'])
downloading = False

def mostrar_spinner():
    global downloading
    downloading = True
    try:
        while downloading:
            sys.stdout.write(f"\rDescargando... {next(spinner_chars)}")
            sys.stdout.flush()
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write('\r' + ' ' * 20 + '\r')  # Limpiar línea

def set_status(status: str):
    pass

def set_progress(progress: int):
    pass

def set_max(new_max: int):
    global downloading
    if not downloading:
        import threading
        threading.Thread(target=mostrar_spinner).start()

def set_progress_callback(progress: int):
    pass

callback = {
    "setStatus": set_status,
    "setProgress": set_progress,
    "setMax": set_max,
    "setDownloadCallback": set_progress_callback
}

def disable_internal_progress():
    minecraft_launcher_lib.utils.get_external_progress_bar = lambda: None

disable_internal_progress()

async def install_minecraft(menu_func):
    global downloading
    os.system('cls')
    print("Selecciona la versión que quieres instalar (o escribe 0 para volver):")
    minecraft_version = input('» ')
    
    if minecraft_version == "0":
        await menu_func()
        return
    
    if minecraft_launcher_lib.utils.is_version_valid(minecraft_version, MINECRAFT_DIRECTORY):
        os.system('cls')
        minecraft_launcher_lib.install.install_minecraft_version(minecraft_version, MINECRAFT_DIRECTORY, callback=callback)
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
        forge = minecraft_launcher_lib.forge.find_forge_version(forge_ver)
        minecraft_launcher_lib.forge.install_forge_version(forge, MINECRAFT_DIRECTORY, callback=callback)
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
    
    if minecraft_launcher_lib.fabric.is_minecraft_version_supported(fabric_ver):
        minecraft_launcher_lib.fabric.install_fabric(fabric_ver, MINECRAFT_DIRECTORY, callback=callback)
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

async def play_mine(menu_func):
    global downloading
    os.system('cls')
    
    with open(CONFIG_JSON, 'r') as file:
        data = json.load(file)
    
    mine_user = data.get('Nombre', 'Player')
    ram = data.get('RAM', 2)

    options = {
        'username': mine_user,
        'uuid': '',
        'token': '',
        "jvmArguments": [f"-Xmx{ram}G", f"-Xms{ram}G"],
        "launcherVersion": LAUNCHER_VERSION
    }

    versiones = minecraft_launcher_lib.utils.get_installed_versions(MINECRAFT_DIRECTORY)
    print("\n▨ Versiones instaladas ▨")
    for version in versiones:
        print(f"» {version['id']}")
    
    print("\nSelecciona una versión (o escribe 0 para volver):")
    version = input('» ')
    
    if version == "0":
        await menu_func()
        return
    
    if minecraft_launcher_lib.utils.is_version_valid(version, MINECRAFT_DIRECTORY):
        downloading = False
        subprocess.run(minecraft_launcher_lib.command.get_minecraft_command(version, MINECRAFT_DIRECTORY, options))
        await menu_func()
    else:
        print("\nERROR: Versión no instalada")
        time.sleep(1.5)
        await play_mine(menu_func)