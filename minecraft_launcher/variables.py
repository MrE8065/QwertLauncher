import os
import minecraft_launcher_lib as mll
LAUNCHER_VERSION = ('1.0')
USER = os.environ['USERNAME']
MINECRAFT_DIRECTORY = mll.utils.get_minecraft_directory()
CONFIG_JSON = f"{MINECRAFT_DIRECTORY}//config.json"