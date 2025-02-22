# Guía para compilar tu propio proyecto de Python

1. Descarga la libreria PyInstaller

    ```
    pip install pyinstaller
    ```

2. Compila el proyecto

    ```
    pyinstaller main.py --onefile --console --icon icon.png --name "QwertLauncher"
    ```

    Vamos a explicar cada una de las opciones utilizadas:
    - ```main.py```: El nombre del archivo principal del proyecto.

    - ```--onefile```: Especifica que el resultado tiene que ser un solo archivo. Se puede cambiar por ```--onedir``` para que se genere un ejecutable y una carpeta con el contenido para que funcione.

    - ```--console```: Especifica que el programa utiliza la consola para mostrarse. Si tu proyecto tuviera una interfaz, utiliza ```--noconsole```.

    - ```--icon```: El icono del ejecutable. Es recomendable un archivo png para que sea compatible con Windows y Linux.

     - ```--name```: El nombre del ejecutable generado.