import sys
import os

# Ruta al directorio de tu proyecto.
# ¡IMPORTANTE! Cambia 'tu_usuario' por tu nombre de usuario de PythonAnywhere
# y 'metadatos_app_pa' por el nombre de la carpeta donde clonaste el repo.
project_home = '/home/tu_usuario/metadatos_app_pa'

# Añade el directorio raíz de tu proyecto al sys.path
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Activar el entorno virtual si es necesario (PythonAnywhere lo maneja en su configuración)
# from dotenv import load_dotenv
# load_dotenv(os.path.join(project_home, '.env')) # Si usas python-dotenv

# Importa tu aplicación Flask. 'app' es el nombre de tu instancia Flask en app.py
from app import app as application # PythonAnywhere busca una variable llamada 'application'
