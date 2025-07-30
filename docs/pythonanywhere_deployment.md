# 🚀 Guía Completa de Deployment en PythonAnywhere

## 📋 **Requisitos Previos**
- ✅ Cuenta en PythonAnywhere creada (`metadatos`)
- ✅ URL disponible: `http://metadatos.pythonanywhere.com/`
- ✅ Código del proyecto preparado

---

## 🔧 **PARTE 1: Deployment en PythonAnywhere**

### **Paso 1: Preparar el Repositorio en GitHub**

1. **Crear repositorio en GitHub** (si no lo tienes):
```bash
# En tu máquina local
git init
git add .
git commit -m "Initial commit - Metadatos App v2.0"
git branch -M main
git remote add origin https://github.com/Gabo-araya/metadatos-app.git
git push -u origin main
```

### **Paso 2: Acceder a PythonAnywhere**

1. **Ir a** [pythonanywhere.com](https://www.pythonanywhere.com)
2. **Iniciar sesión** con usuario `metadatos`
3. **Abrir Dashboard**

### **Paso 3: Configurar Bash Console**

1. **Ir a la pestaña "Consoles"**
2. **Abrir "Bash" console**
3. **Ejecutar los siguientes comandos**:

```bash
# Verificar ubicación actual
pwd
# Debería mostrar: /home/metadatos

# Clonar el repositorio
git clone https://github.com/Gabo-araya/metadatos-app.git metadatos_app
cd metadatos_app

# Verificar que los archivos están ahí
ls -la
```

### **Paso 4: Crear y Configurar Entorno Virtual**

```bash
# Crear entorno virtual con Python 3.10
mkvirtualenv --python=/usr/bin/python3.10 env

# Verificar que el entorno está activo (debe aparecer (env) al inicio)
# Si no está activo, activarlo:
workon env

# Actualizar pip
pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt

# Verificar instalación
pip list
```

### **Paso 5: Configurar Variables de Entorno**

```bash
# Crear archivo .env
nano .env
```

**Contenido del archivo .env**:
```env
# Configuración básica
SECRET_KEY=tu-clave-secreta-super-fuerte-para-produccion-cambiar-esto
FLASK_ENV=production
FLASK_DEBUG=False

# Base de datos
DATABASE_URL=sqlite:///metadatos.db

# Credenciales admin (CAMBIAR ESTOS VALORES)
ADMIN_USERNAME=admin_metadatos
ADMIN_PASSWORD=Password_Super_Segura_2024!

# Configuración de archivos
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216

# Configuración de seguridad
SESSION_COOKIE_SECURE=False
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax

# Logging
LOG_LEVEL=INFO
LOG_FILE=app.log

# Metadatos Dublin Core
DC_CREATOR=Metadatos App Team
DC_PUBLISHER=Metadatos App
DC_RIGHTS=© 2024 Metadatos App. Todos los derechos reservados.
DC_LANGUAGE=es

# URL base
BASE_URL=http://metadatos.pythonanywhere.com
```

**Guardar y salir**: `Ctrl + X`, luego `Y`, luego `Enter`

### **Paso 6: Inicializar Base de Datos y Crear Directorios**

```bash
# Crear directorios necesarios
mkdir -p uploads
mkdir -p logs

# Dar permisos
chmod 755 uploads
chmod 755 logs

# Inicializar base de datos
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('✅ Base de datos inicializada')"

# Verificar que se creó la BD
ls -la *.db
```

### **Paso 7: Probar la Aplicación Localmente en PythonAnywhere**

```bash
# Probar que la app funciona
python app.py &
# Debería mostrar algo como "Running on http://127.0.0.1:5000"

# Si funciona, detener el proceso
pkill -f "python app.py"
```

### **Paso 8: Configurar Web App en PythonAnywhere**

1. **Ir a la pestaña "Web"** en el dashboard
2. **Click en "Add a new web app"**
3. **Seleccionar el dominio**: `metadatos.pythonanywhere.com`
4. **Seleccionar "Manual configuration"**
5. **Seleccionar "Python 3.10"**
6. **Click "Next"**

### **Paso 9: Configurar el Archivo WSGI**

1. **En la página de configuración Web**, buscar **"Code" section**
2. **Click en el enlace del "WSGI configuration file"**
3. **Reemplazar TODO el contenido** con:

```python
import sys
import os
from pathlib import Path

# Configurar la ruta del proyecto
project_home = '/home/metadatos/metadatos_app'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Cargar variables de entorno
from dotenv import load_dotenv
env_path = Path(project_home) / '.env'
if env_path.exists():
    load_dotenv(env_path)

# Importar la aplicación
os.chdir(project_home)
from wsgi import application

# Para debug (remover en producción)
print(f"WSGI configurado desde: {project_home}")
print(f"Python path: {sys.path[:2]}")
```

4. **Guardar el archivo**: `Ctrl + S`

### **Paso 10: Configurar el Entorno Virtual en Web App**

1. **En la sección "Virtualenv"** de la página Web
2. **Introducir la ruta**: `/home/metadatos/.virtualenvs/env`
3. **Click en el checkbox para confirmar**

### **Paso 11: Configurar Archivos Estáticos**

1. **En la sección "Static files"**
2. **Agregar las siguientes entradas**:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/metadatos/metadatos_app/static/` |
| `/uploads/` | `/home/metadatos/metadatos_app/uploads/` |

### **Paso 12: Configurar Source Code**

1. **En la sección "Code"**
2. **Source code**: `/home/metadatos/metadatos_app`
3. **Working directory**: `/home/metadatos/metadatos_app`

### **Paso 13: Reload y Probar**

1. **Click en el botón verde "Reload"**
2. **Esperar a que termine el reload**
3. **Click en el enlace** `http://metadatos.pythonanywhere.com/`
4. **Debería abrir la aplicación funcionando**

### **Paso 14: Verificar Funcionalidades**

1. **Probar la página principal** - Debería mostrar "No hay archivos disponibles"
2. **Ir a `/login`** - Probar login con las credenciales del .env
3. **Subir un archivo de prueba** en el panel admin
4. **Verificar que se muestra** en la página principal
