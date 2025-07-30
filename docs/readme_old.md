# Metadatos App

Una aplicación web desarrollada con Flask y SQLite para la gestión y visualización de archivos con metadatos, siguiendo los estándares de Dublin Core. La aplicación incluye un panel de administración para subir y gestionar archivos, y una landing page pública para visualizarlos.

---

## **Características**

* **Gestión de Archivos**: Sube archivos con un título y una descripción.
* **Panel de Administración**: Acceso restringido para un solo usuario (configurable) para subir y eliminar archivos.
* **Landing Page Pública**: Muestra todos los archivos subidos de forma organizada.
* **Sección de Ayuda**: Información detallada sobre la aplicación y los metadatos Dublin Core.
* **Metadatos Dublin Core**: Integración de elementos clave de Dublin Core en las plantillas HTML para una mejor indexación y descripción de los recursos.
* **Base de Datos SQLite**: Almacenamiento ligero y eficiente de los metadatos de los archivos.

---

## **Tecnologías Utilizadas**

* **Backend**: Python 3, Flask, Flask-SQLAlchemy, Werkzeug
* **Base de Datos**: SQLite
* **Frontend**: HTML5, CSS3

---

## **Estructura del Proyecto**

```

metadatos/
├── app.py                  \# Lógica principal de la aplicación Flask
├── database.py             \# Configuración de la base de datos y modelo de archivos
├── templates/              \# Archivos HTML (Jinja2)
│   ├── base.html           \# Plantilla base con metadatos Dublin Core
│   ├── index.html          \# Landing page principal
│   ├── admin.html          \# Panel de administración
│   ├── login.html          \# Página de login para el admin
│   └── help.html           \# Sección de ayuda
├── static/                 \# Archivos estáticos (CSS, JS)
│   ├── css/
│   │   └── style.css       \# Estilos CSS básicos
│   └── js/
│       └── script.js       \# (Opcional) Scripts JavaScript
├── uploads/                \# Directorio para los archivos subidos (NO SUBIR AL REPO)
├── .gitignore              \# Archivo para ignorar en Git
├── requirements.txt        \# Dependencias de Python
└── wsgi.py                 \# (Para PythonAnywhere) Punto de entrada WSGI

````

---

## **Configuración e Instalación Local**

Sigue estos pasos para poner en marcha el proyecto en tu entorno local:

1.  **Clonar el Repositorio:**
    ```bash
    git clone [https://github.com/TuUsuario/metadatos-app.git](https://github.com/TuUsuario/metadatos-app.git)
    cd metadatos-app
    ```

2.  **Crear un Entorno Virtual (Recomendado):**
    ```bash
    python -m venv venv
    # En Windows:
    venv\Scripts\activate
    # En macOS/Linux:
    source venv/bin/activate
    ```

3.  **Instalar Dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ejecutar la Aplicación:**
    ```bash
    python app.py
    ```
    La aplicación estará disponible en `http://127.0.0.1:5000/`.

---

## **Uso de la Aplicación**

* **Página Principal (`/`)**: Muestra los archivos subidos.
* **Ayuda (`/help`)**: Proporciona información sobre la aplicación y Dublin Core.
* **Login (`/login`)**: Inicia sesión para acceder al panel de administración.
    * **Usuario por defecto**: `admin`
    * **Contraseña por defecto**: `adminpass`
    * **¡ADVERTENCIA!** Cambia estas credenciales en `app.py` para producción y utiliza una contraseña segura.
* **Panel de Administración (`/admin`)**:
    * Sube nuevos archivos con un título y una descripción.
    * Visualiza y elimina archivos existentes.

---
