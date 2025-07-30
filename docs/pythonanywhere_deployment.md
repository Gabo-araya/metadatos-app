
## **Despliegue en PythonAnywhere**

Para desplegar esta aplicación en PythonAnywhere, sigue estos pasos clave:

1.  **Preparar tu Repositorio:**
    * Asegúrate de que tu rama `main` o `master` en GitHub esté actualizada con la última versión de tu código.

2.  **Configurar PythonAnywhere:**
    * Crea una cuenta en [PythonAnywhere](https://www.pythonanywhere.com/).
    * Ve a la pestaña **Web** y haz clic en "Add a new web app".
    * Selecciona el framework **Flask**.
    * Elige la versión de Python (ej. Python 3.9).

3.  **Clonar tu Repositorio en PythonAnywhere:**
    * En la pestaña **Consoles**, abre una nueva "Bash console".
    * Navega a la ubicación donde quieras clonar tu proyecto (por ejemplo, `cd /home/tu_usuario/`).
    * Clona tu repositorio:
        ```bash
        git clone [https://github.com/Gabo-araya/metadatos-app.git](https://github.com/Gabo-araya/metadatos-app.git) metadatos_app_pa
        # Asegúrate de usar un nombre de carpeta descriptivo, ej. metadatos_app_pa
        ```
    * Navega a la carpeta de tu proyecto: `cd metadatos_app_pa`

4.  **Crear y Activar un Entorno Virtual en PythonAnywhere:**
    ```bash
    mkvirtualenv --python=/usr/bin/python3.9 venv_metadatos # Ajusta la versión de Python si es necesario
    source ~/.virtualenvs/venv_metadatos/bin/activate
    ```

5.  **Instalar Dependencias en PythonAnywhere:**
    ```bash
    pip install -r requirements.txt
    ```

6.  **Configurar el Archivo `wsgi.py`:**
    * En PythonAnywhere, ve a la página de configuración de tu aplicación web (Web tab).
    * En la sección "Code", busca "WSGI configuration file".
    * Edita este archivo (normalmente `/var/www/tu_usuario_pythonanywhere_com_wsgi.py`).
    * Reemplaza el contenido por algo similar a esto, asegurándote de que la ruta sea correcta:

    ```python
    import sys
    import os

    # Añade el directorio raíz de tu proyecto al sys.path
    project_home = '/home/tu_usuario/metadatos_app_pa' # <--- ¡CAMBIA ESTO!
    if project_home not in sys.path:
        sys.path.insert(0, project_home)

    # Importa y ejecuta tu aplicación Flask
    from app import app as application # 'application' es el nombre que PythonAnywhere espera
    ```

7.  **Actualizar la Base de Datos (Primera Vez):**
    * En una Bash console, navega a tu directorio de proyecto (`cd /home/tu_usuario/metadatos_app_pa`).
    * Asegúrate de que tu entorno virtual esté activado (`source ~/.virtualenvs/venv_metadatos/bin/activate`).
    * Ejecuta un script para inicializar la base de datos (puedes crear un `init_db.py` simple o ejecutar una sección de `app.py`):
        ```python
        # Opcional: crea un archivo init_db.py:
        # from app import app, db, init_db
        # with app.app_context():
        #     db.create_all()

        # Luego ejecútalo:
        # python init_db.py
        ```
        O, dado que `init_db(app)` se llama en `app.py` con `app.before_first_request`, la base de datos se creará la primera vez que la aplicación se cargue en PythonAnywhere. Sin embargo, para asegurarte, puedes acceder a la app después de configurarla.

8.  **Configurar Variables de Entorno (Importante para `SECRET_KEY` y credenciales):**
    * Nunca pongas la `SECRET_KEY` o contraseñas directamente en tu código en producción.
    * En PythonAnywhere, en la página de tu aplicación web, en la sección "Environment variables", puedes añadir variables como:
        * `FLASK_SECRET_KEY = TU_CLAVE_ALEATORIA_MUY_LARGA`
    * Luego, en `app.py`, la accederías así: `app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'supersecretkey_dev')`

9.  **Recargar la Aplicación:**
    * Vuelve a la pestaña **Web** de PythonAnywhere y haz clic en el botón "Reload" (verde).

¡Tu aplicación debería estar funcionando en la URL de PythonAnywhere!

---
