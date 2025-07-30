#!/usr/bin/env python3
"""
WSGI Configuration for Metadatos App
Configuración mejorada para despliegue en PythonAnywhere y otros servidores WSGI
"""

import sys
import os
from pathlib import Path

# ===== CONFIGURACIÓN DE RUTAS =====
# Obtener la ruta del directorio del proyecto
project_root = Path(__file__).parent.absolute()

# Para PythonAnywhere, ajusta esta ruta según tu configuración
# Ejemplo: /home/tu_usuario/metadatos_app
# project_root = Path('/home/tu_usuario/metadatos_app')

# Agregar el directorio del proyecto al sys.path
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# ===== CONFIGURACIÓN DE ENTORNO VIRTUAL =====
# Solo necesario si no usas el sistema de entornos virtuales de PythonAnywhere
# venv_path = project_root / 'venv' / 'lib' / 'python3.9' / 'site-packages'
# if venv_path.exists() and str(venv_path) not in sys.path:
#     sys.path.insert(0, str(venv_path))

# ===== CONFIGURACIÓN DE VARIABLES DE ENTORNO =====
try:
    from dotenv import load_dotenv
    # Cargar variables de entorno desde .env
    env_path = project_root / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✅ Variables de entorno cargadas desde: {env_path}")
    else:
        print(f"⚠️ Archivo .env no encontrado en: {env_path}")
except ImportError:
    print("⚠️ python-dotenv no está instalado. Las variables de entorno se cargarán del sistema.")

# ===== CONFIGURACIÓN DE LOGGING =====
import logging
from logging.handlers import RotatingFileHandler

# Configurar logging para producción
log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
log_file = project_root / (os.environ.get('LOG_FILE', 'app.log'))
log_max_size = int(os.environ.get('LOG_MAX_SIZE', '10')) * 1024 * 1024  # MB a bytes
log_max_files = int(os.environ.get('LOG_MAX_FILES', '5'))

# Crear directorio de logs si no existe
log_file.parent.mkdir(exist_ok=True)

# Configurar el handler de logs
file_handler = RotatingFileHandler(
    str(log_file),
    maxBytes=log_max_size,
    backupCount=log_max_files
)

file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))

file_handler.setLevel(getattr(logging, log_level, logging.INFO))

# ===== IMPORTAR Y CONFIGURAR LA APLICACIÓN =====
try:
    from app import app as application

    # Configurar el logging de la aplicación
    if not application.debug:
        application.logger.addHandler(file_handler)
        application.logger.setLevel(getattr(logging, log_level, logging.INFO))

        # Log de inicio
        application.logger.info('=== Metadatos App iniciando ===')
        application.logger.info(f'Directorio del proyecto: {project_root}')
        application.logger.info(f'Python path: {sys.path[:3]}...')
        application.logger.info(f'Variables de entorno cargadas: {bool(os.environ.get("SECRET_KEY"))}')

    print("✅ Aplicación Flask cargada correctamente")

except ImportError as e:
    error_msg = f"❌ Error al importar la aplicación: {e}"
    print(error_msg)

    # Crear una aplicación de emergencia para mostrar el error
    from flask import Flask
    application = Flask(__name__)

    @application.route('/')
    def error():
        return f"""
        <html>
            <head><title>Error de Configuración</title></head>
            <body style="font-family: Arial; padding: 20px; background: #f8f9fa;">
                <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <h1 style="color: #dc3545;">Error de Configuración</h1>
                    <p><strong>No se pudo cargar la aplicación Metadatos App.</strong></p>
                    <p><strong>Error:</strong> {e}</p>
                    <p><strong>Directorio actual:</strong> {project_root}</p>
                    <p><strong>Python path:</strong> {sys.path[0]}</p>

                    <h3>Pasos para solucionar:</h3>
                    <ol>
                        <li>Verifica que todos los archivos estén en el directorio correcto</li>
                        <li>Asegúrate de que las dependencias estén instaladas: <code>pip install -r requirements.txt</code></li>
                        <li>Revisa la configuración del archivo .env</li>
                        <li>Contacta al administrador si el problema persiste</li>
                    </ol>

                    <hr style="margin: 20px 0;">
                    <small style="color: #6c757d;">
                        Si estás viendo este mensaje en producción, hay un problema de configuración que debe resolverse inmediatamente.
                    </small>
                </div>
            </body>
        </html>
        """, 500

except Exception as e:
    error_msg = f"❌ Error inesperado al configurar la aplicación: {e}"
    print(error_msg)

    # Log del error si es posible
    try:
        logging.error(error_msg, exc_info=True)
    except:
        pass

    # Re-raise para que el servidor WSGI pueda manejar el error
    raise

# ===== CONFIGURACIÓN ADICIONAL PARA PRODUCCIÓN =====
if not getattr(application, 'debug', True):
    # Configuración adicional para producción

    # Configurar cabeceras de seguridad
    @application.after_request
    def add_security_headers(response):
        # Prevenir ataques XSS
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'

        # HSTS (solo si se usa HTTPS)
        if application.config.get('SESSION_COOKIE_SECURE'):
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'

        # CSP básico
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "img-src 'self' data: https:; "
            "font-src 'self' https://cdn.jsdelivr.net;"
        )

        return response

    # Handler para errores 500
    @application.errorhandler(500)
    def internal_error(error):
        application.logger.error(f'Error 500: {error}', exc_info=True)
        return """
        <html>
            <head><title>Error Interno</title></head>
            <body style="font-family: Arial; padding: 20px; text-align: center; background: #f8f9fa;">
                <div style="max-width: 500px; margin: 50px auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <h1 style="color: #dc3545;">Error Interno del Servidor</h1>
                    <p>Lo sentimos, ha ocurrido un error interno.</p>
                    <p>El error ha sido registrado y será revisado.</p>
                    <a href="/" style="display: inline-block; margin-top: 20px; padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 4px;">Volver al Inicio</a>
                </div>
            </body>
        </html>
        """, 500

# ===== INFORMACIÓN DE DEBUG =====
def print_debug_info():
    """Imprime información útil para debugging"""
    print("\n" + "="*50)
    print("METADATOS APP - INFORMACIÓN DE DEBUG")
    print("="*50)
    print(f"Directorio del proyecto: {project_root}")
    print(f"Directorio actual: {os.getcwd()}")
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    print(f"Modo debug: {getattr(application, 'debug', 'Unknown')}")
    print(f"Variables de entorno importantes:")

    env_vars = ['SECRET_KEY', 'DATABASE_URL', 'UPLOAD_FOLDER', 'ADMIN_USERNAME']
    for var in env_vars:
        value = os.environ.get(var, 'No configurada')
        # Ocultar valores sensibles
        if var in ['SECRET_KEY', 'ADMIN_PASSWORD'] and value != 'No configurada':
            value = '*' * 8
        print(f"  {var}: {value}")

    print(f"Archivos en el directorio:")
    try:
        files = list(project_root.glob('*.py'))[:10]  # Mostrar solo los primeros 10
        for file in files:
            print(f"  ✓ {file.name}")
        if len(list(project_root.glob('*.py'))) > 10:
            print(f"  ... y {len(list(project_root.glob('*.py'))) - 10} más")
    except Exception as e:
        print(f"  Error al listar archivos: {e}")

    print("="*50 + "\n")

# Mostrar información de debug solo en desarrollo
if os.environ.get('FLASK_DEBUG') == 'True' or '--debug' in sys.argv:
    print_debug_info()

# ===== FUNCIÓN DE VALIDACIÓN =====
def validate_configuration():
    """Valida que la configuración sea correcta"""
    errors = []

    # Verificar variables críticas
    if not os.environ.get('SECRET_KEY'):
        errors.append("SECRET_KEY no está configurada")

    if not os.environ.get('ADMIN_USERNAME'):
        errors.append("ADMIN_USERNAME no está configurada")

    if not os.environ.get('ADMIN_PASSWORD'):
        errors.append("ADMIN_PASSWORD no está configurada")

    # Verificar archivos críticos
    critical_files = ['app.py', 'database.py']
    for file in critical_files:
        if not (project_root / file).exists():
            errors.append(f"Archivo crítico no encontrado: {file}")

    # Verificar directorio de uploads
    upload_dir = project_root / os.environ.get('UPLOAD_FOLDER', 'uploads')
    if not upload_dir.exists():
        try:
            upload_dir.mkdir(parents=True, exist_ok=True)
            print(f"✅ Directorio de uploads creado: {upload_dir}")
        except Exception as e:
            errors.append(f"No se pudo crear el directorio de uploads: {e}")

    if errors:
        error_msg = "❌ Errores de configuración encontrados:\n" + "\n".join(f"  - {error}" for error in errors)
        print(error_msg)
        if hasattr(application, 'logger'):
            application.logger.error(error_msg)
        return False

    print("✅ Validación de configuración completada exitosamente")
    return True

# Ejecutar validación
if not validate_configuration():
    print("⚠️ La aplicación puede no funcionar correctamente debido a errores de configuración")

# ===== PUNTO DE ENTRADA PRINCIPAL =====
if __name__ == "__main__":
    # Si se ejecuta directamente (no recomendado para producción)
    print("⚠️ Ejecutando WSGI directamente. Para desarrollo usa: flask run")
    print("⚠️ Para producción usa un servidor WSGI como Gunicorn")

    port = int(os.environ.get('FLASK_RUN_PORT', 5000))
    host = os.environ.get('FLASK_RUN_HOST', '127.0.0.1')
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

    application.run(host=host, port=port, debug=debug)

# ===== INFORMACIÓN FINAL =====
print(f"🚀 WSGI configurado correctamente para Metadatos App")
print(f"📂 Proyecto: {project_root}")
print(f"🐍 Python: {sys.version.split()[0]}")

# Exportar application para el servidor WSGI
# Esta es la variable que buscan los servidores WSGI como Gunicorn, uWSGI, etc.
__all__ = ['application']



#=====================================================

# import sys
# import os

# # Ruta al directorio de tu proyecto.
# # ¡IMPORTANTE! Cambia 'tu_usuario' por tu nombre de usuario de PythonAnywhere
# # y 'metadatos_app_pa' por el nombre de la carpeta donde clonaste el repo.
# project_home = '/home/tu_usuario/metadatos_app_pa'

# # Añade el directorio raíz de tu proyecto al sys.path
# if project_home not in sys.path:
#     sys.path.insert(0, project_home)

# # Activar el entorno virtual si es necesario (PythonAnywhere lo maneja en su configuración)
# # from dotenv import load_dotenv
# # load_dotenv(os.path.join(project_home, '.env')) # Si usas python-dotenv

# # Importa tu aplicación Flask. 'app' es el nombre de tu instancia Flask en app.py
# from app import app as application # PythonAnywhere busca una variable llamada 'application'
