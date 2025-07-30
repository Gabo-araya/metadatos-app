#!/usr/bin/env python3
"""
WSGI Simple para Docker - Sin logging complejo
"""
import sys
import os
from pathlib import Path

# Configuración básica de rutas
project_root = Path(__file__).parent.absolute()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Cargar variables de entorno
try:
    from dotenv import load_dotenv
    env_path = project_root / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✅ Variables de entorno cargadas desde: {env_path}")
except ImportError:
    print("⚠️ python-dotenv no disponible, usando variables del sistema")

# Crear directorios necesarios si no existen
for dir_name in ['uploads', 'logs', 'data']:
    dir_path = project_root / dir_name
    if not dir_path.exists():
        try:
            dir_path.mkdir(exist_ok=True)
            print(f"✅ Directorio creado: {dir_path}")
        except Exception as e:
            print(f"⚠️ Error creando directorio {dir_path}: {e}")

# Importar la aplicación Flask
try:
    from app import app as application
    print("✅ Aplicación Flask cargada correctamente")
    
    # Configuración básica para producción
    if not application.debug:
        # Solo logging básico a consola
        import logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s: %(message)s'
        )
        application.logger.info('=== Metadatos App iniciando (Docker) ===')
    
except Exception as e:
    print(f"❌ Error cargando aplicación: {e}")
    raise

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5000, debug=False)
