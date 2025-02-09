import os
import time
import json

from .variables import *
from .minecraft import install_fabric, install_forge, install_minecraft, play_mine


async def check():
    os.system('cls' if os.name == 'nt' else 'clear')
    if not os.path.exists(MINECRAFT_DIRECTORY):
        os.makedirs(MINECRAFT_DIRECTORY)

    if not os.path.exists(CONFIG_JSON):
        # Si el archivo JSON no existe, crea uno vacío
        with open(CONFIG_JSON, 'w') as f:
            print("Archivo config.json no encontrado.")
            time.sleep(1)
            print("Se ha creado el archivo config.json.")
            time.sleep(2)
            os.system('cls' if os.name == 'nt' else 'clear')
            print('Introduce un nombre de usuario:')
            nombre = input('» ')
            if nombre == "":
                print('Nombre no válido')
                time.sleep(2)
                await check()
            else:
                print('Introduce cuánta RAM se utilizará (4GB recomendado):')
                ram = input('» ')
                if ram == "":
                    print('RAM no válida')
                    time.sleep(2)
                    await check()
                else:
                    data = {
                        "Nombre": nombre,
                        "RAM": ram,
                    }
                    with open(CONFIG_JSON, 'w') as file:
                        json.dump(data, file)
                    print("◈ Guardando... ◈")
                    time.sleep(2)
                    await menu_I()
    else:
        # Si el archivo JSON existe, pero está vacío, accede a él
        if os.stat(CONFIG_JSON).st_size == 0:
            print("El archivo config.json está vacío.")
            time.sleep(1)
            os.system('cls' if os.name == 'nt' else 'clear')
            print('Introduce un nombre de usuario:')
            nombre = input('» ')
            if nombre == "":
                print('Nombre no válido')
                time.sleep(2)
                await check()
            else:
                print('Introduce cuánta RAM se utilizará (4GB recomendado):')
                ram = input('» ')
                if ram == "":
                    print('RAM no válida')
                    time.sleep(2)
                    await check()
                else:
                    data = {
                        "Nombre": nombre,
                        "RAM": ram,
                    }
                    with open(CONFIG_JSON, 'w') as file:
                        json.dump(data, file)
                    print("◈ Guardando... ◈")
                    time.sleep(2)
                    await menu_I()
        else:
            await menu_I()
            
async def menu_I():
    
    os.system('cls' if os.name == 'nt' else 'clear')
    with open(CONFIG_JSON, 'r') as file:
        data = json.load(file)
    nombre = data.get('Nombre')
    
    print(
        f'''
                    ██╗  ██╗ ██╗    ██╗   ██╗ ████    ██╗
                    ╚██╗██╔╝░██║░░░░██║░░░██║░██║██░░░██║
                    ░╚███╔╝░░██║░░░░██║░░░██║░██║░██░░██║
                    ░██╔██╗░░██║░░░░██║░░░██║░██║░░██░██║
                    ██╔╝╚██╗░██████╗████████║░██║░░░████║
                    ╚═╝░░╚═╝░╚═════╝╚═══════╝ ╚═╝   ╚═══╝ {LAUNCHER_VERSION}

Bienvenido a QwertLauncher, {nombre}\n

▐Jugar (1)
▐Instalar Minecraft (2)
▐Instalar Forge (3)
▐Instalar Fabric (4)
▐Editar configuración (5)
▐---------------------------
▐Salir (0)
''')

    select = input('▐Elige una opción: ')
    if select == "1":
        await play_mine(menu_I)
    if select == "2":
        await install_minecraft(menu_I)
    if select == "3":
        await install_forge(menu_I)
    if select == "4":
        await install_fabric(menu_I)
    if select == '5':
        await cambiar_config()
    if select == "0":
        os.system('cls' if os.name == 'nt' else 'clear')
        time.sleep(0.5)
        print("Adiós :)")
        time.sleep(2)
        exit()
    if select == "":
        await menu_I()
        
async def cambiar_config():
    
    #Cargar configuration.json
    with open(CONFIG_JSON, 'r') as file:
        data = json.load(file)

    #Mostrar la config actual y el diálogo para cambiarla
    os.system('cls' if os.name == 'nt' else 'clear')
    print("▨ Valores actuales ▨")
    for key, value in data.items():
        print(f"▸ {key}: {value}")
    print('\n▐¿Qué dato desea cambiar? (o escribe 0 para volver) \n  (Nombre/RAM)')
    option = input('» ')
    if option == "0":
        await menu_I()
    else:
        if option in data:
            if option=="Nombre":
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f'▐Ingresa el nuevo nombre')
            elif option=="RAM":
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f'▐Ingresa cuanta RAM quieres que se utilice')
                
            nuevo_valor = input('» ')
            data[option] = nuevo_valor

            with open(CONFIG_JSON, 'w') as file:
                json.dump(data, file)
                
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"◈ Actualizando... ◈")
            time.sleep(1.5)
            await menu_I()
        else:
            print("Opción no válida. Por favor, elige entre Nombre o RAM.")
            time.sleep(1.5)
            await cambiar_config()