def show_error(message: str):
    """
    Muestra un mensaje de error.

    Ejemplo:

      [ERROR] Algo a ocurrido mal :(
    """
    print(f"\u001b[31m[ERROR]:\u001b[0m {message}")


def show_success(message: str):
    """
    Muestra un mensaje de éxito.

    Ejemplo:

      [SUCCESS] El proceso se completó
    """
    print(f"\u001b[32m[SUCCESS]:\u001b[0m {message}")


def show_warn(message: str):
    """
    Muestra un mensaje de advertencia.

    Ejemplo:

      [WARN] Saltando pasos...
    """
    print(f"\u001b[33m[WARN]:\u001b[0m {message}")


def show_info(message: str):
    """
    Muestra un mensaje de información.

    Ejemplo:

      [INFO] Ha pasado algo
    """
    print(f"\u001b[34m[INFO]:\u001b[0m {message}")
