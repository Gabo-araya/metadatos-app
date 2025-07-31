# 📁 Metadatos App

Una aplicación web desarrollada con Flask para la gestión integral de archivos digitales con soporte completo para metadatos Dublin Core.
Incluye un panel de administración, sistema de búsqueda, y una interfaz pública responsive.

![Python](https://img.shields.io/badge/python-3.8+-brightgreen.svg)
![Flask](https://img.shields.io/badge/flask-3.0+-red.svg)
![Bootstrap](https://img.shields.io/badge/bootstrap-5.3-purple.svg)

---

## 🚀 **Características Principales**

### ✨ **Funcionalidades Core**
- **📤 Gestión de Archivos**: Subida segura con validación de tipos y tamaños
- **🔐 Panel de Administración**: Acceso protegido con autenticación robusta
- **🌐 Landing Page Pública**: Interfaz moderna y responsive para visualizar archivos
- **📖 Sistema de Ayuda**: Documentación completa integrada
- **🏷️ Metadatos Dublin Core**: Estándares internacionales para mejor indexación
- **🔍 Búsqueda Avanzada**: Sistema de búsqueda por título, descripción y palabras clave
- **📱 Diseño Responsive**: Optimizado para dispositivos móviles y escritorio

### 🛡️ **Seguridad y Calidad**
- **🔒 Autenticación Segura**: Hash de contraseñas con Werkzeug
- **✅ Validación de Archivos**: Tipos permitidos y límites de tamaño
- **🚫 Protección XSS**: Sanitización de nombres de archivos
- **📊 Logging Completo**: Registro de actividades y errores
- **🔧 Manejo de Errores**: Páginas de error personalizadas y recuperación graceful

### 🎨 **Experiencia de Usuario**
- **⚡ Interfaz Moderna**: Bootstrap 5.3 con componentes personalizados
- **🎭 Animaciones Suaves**: Transiciones CSS y efectos interactivos
- **♿ Accesibilidad**: Soporte para lectores de pantalla y navegación por teclado
- **📄 Paginación**: Navegación eficiente para grandes colecciones
- **🏷️ Iconos Dinámicos**: Iconos específicos por tipo de archivo

---

## 🏗️ **Arquitectura y Tecnologías**

### **Backend**
- **Python 3.8+** - Lenguaje principal
- **Flask 3.0** - Framework web minimalista y potente
- **SQLAlchemy** - ORM para manejo de base de datos
- **SQLite** - Base de datos ligera y eficiente
- **Werkzeug** - Utilidades WSGI y seguridad

### **Frontend**
- **HTML5** - Estructura moderna y semántica
- **CSS3** - Estilos avanzados con Grid y Flexbox
- **JavaScript ES6+** - Interactividad y mejoras UX
- **Bootstrap 5.3** - Framework CSS responsive
- **Bootstrap Icons** - Iconografía consistente

### **Estándares y Metadatos**
- **Dublin Core** - Metadatos estándar para recursos digitales
- **Schema.org** - Datos estructurados para SEO
- **Open Graph** - Metadatos para redes sociales
- **WCAG 2.1** - Pautas de accesibilidad web

---

## 📁 **Estructura del Proyecto**

```
metadatos_app/
├── 📄 app.py                      # Aplicación Flask principal
├── 📄 database.py                 # Modelos y configuración de BD
├── 📄 wsgi.py                     # Configuración WSGI mejorada
├── 📄 requirements.txt            # Dependencias Python
├── 📄 .env.example               # Variables de entorno de ejemplo
├── 📄 README.md                  # Esta documentación
├── 📁 templates/                 # Plantillas Jinja2
│   ├── 📄 base.html              # Plantilla base con Dublin Core
│   ├── 📄 index.html             # Página principal pública
│   ├── 📄 admin.html             # Panel de administración
│   ├── 📄 login.html             # Página de autenticación
│   ├── 📄 help.html              # Centro de ayuda
│   └── 📄 file_detail.html       # Vista detallada de archivos
├── 📁 static/                    # Recursos estáticos
│   ├── 📁 css/
│   │   └── 📄 style.css          # Estilos personalizados
│   ├── 📁 js/
│   │   └── 📄 script.js          # JavaScript interactivo
│   └── 📄 favicon.ico           # Icono de la aplicación
├── 📁 uploads/                   # Archivos subidos (no en repo)
├── 📁 logs/                      # Archivos de log (no en repo)
└── 📁 docs/                      # Documentación adicional
    └── 📄 comandos.md            # Comandos útiles de desarrollo
```

---

## 🚀 **Instalación y Configuración**

### **Prerrequisitos**
- Python 3.8 o superior
- Git
- Navegador web moderno

### **1. Clonar el Repositorio**
```bash
git clone https://github.com/Gabo-araya/metadatos-app.git
cd metadatos-app
```

### **2. Configurar Entorno Virtual**
```bash
# Crear entorno virtual
python3 -m venv env

# Activar entorno virtual
# En Linux/macOS:
source env/bin/activate
# En Windows:
env\Scripts\activate
```

### **3. Instalar Dependencias**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### **4. Configurar Variables de Entorno**
```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus configuraciones
nano .env  # o tu editor preferido
```

**Variables críticas a configurar:**
```env
SECRET_KEY=tu-clave-secreta-muy-fuerte-aqui
ADMIN_USERNAME=tu_admin_user
ADMIN_PASSWORD=tu_contraseña_super_segura
DATABASE_URL=sqlite:///metadatos.db
UPLOAD_FOLDER=uploads
```

### **5. Inicializar Base de Datos**
```bash
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Base de datos inicializada')"
```

### **6. Ejecutar la Aplicación**
```bash
# Modo desarrollo
flask run

# O directamente con Python
python app.py
```

La aplicación estará disponible en: **http://127.0.0.1:5000**

---

## 🌐 **Despliegue en PythonAnywhere**

### **Prerrequisitos**
- ✅ Cuenta en PythonAnywhere con usuario `metadatos`
- ✅ URL disponible: `http://metadatos.pythonanywhere.com/`
- ✅ Código del proyecto en GitHub

### **Paso 1: Preparar el Repositorio**

```bash
# En tu máquina local, asegurar que el código esté en GitHub
git add .
git commit -m "Ready for PythonAnywhere deployment"
git push origin main
```

### **Paso 2: Configurar en PythonAnywhere**

1. **Iniciar sesión** en [pythonanywhere.com](https://www.pythonanywhere.com) con usuario `metadatos`
2. **Abrir "Bash" console** desde el dashboard
3. **Clonar el repositorio**:

```bash
# Verificar ubicación actual
pwd  # Debería mostrar: /home/metadatos

# Clonar el repositorio
git clone https://github.com/Gabo-araya/metadatos-app.git metadatos_app
cd metadatos_app
```

### **Paso 3: Configurar Entorno Virtual**

```bash
# Crear entorno virtual con Python 3.10
mkvirtualenv --python=/usr/bin/python3.10 env

# Si no está activo, activarlo:
workon env

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt
```

### **Paso 4: Configurar Variables de Entorno**

```bash
# Crear archivo .env
nano .env
```

**Contenido del archivo .env**:
```env
# Configuración básica (CAMBIAR ESTOS VALORES)
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

# URL base
BASE_URL=http://metadatos.pythonanywhere.com

# Metadatos Dublin Core
DC_CREATOR=Metadatos App Team
DC_PUBLISHER=Metadatos App
DC_RIGHTS=© 2024 Metadatos App. Todos los derechos reservados.
DC_LANGUAGE=es
```

**Guardar**: `Ctrl + X`, `Y`, `Enter`

### **Paso 5: Inicializar Base de Datos**

```bash
# Crear directorios necesarios
mkdir -p uploads logs
chmod 755 uploads logs

# Inicializar base de datos
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('✅ Base de datos inicializada')"
```

### **Paso 6: Configurar Web App**

1. **Ir a la pestaña "Web"** en el dashboard
2. **Click "Add a new web app"**
3. **Seleccionar dominio**: `metadatos.pythonanywhere.com`
4. **Seleccionar "Manual configuration"**
5. **Seleccionar "Python 3.10"**

### **Paso 7: Configurar WSGI**

1. **En la configuración Web**, click en **"WSGI configuration file"**
2. **Reemplazar TODO el contenido** con:

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
```

### **Paso 8: Configurar Paths**

1. **Virtualenv**: `/home/metadatos/.virtualenvs/env`
2. **Source code**: `/home/metadatos/metadatos_app`
3. **Working directory**: `/home/metadatos/metadatos_app`

### **Paso 9: Configurar Archivos Estáticos**

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/metadatos/metadatos_app/static/` |
| `/uploads/` | `/home/metadatos/metadatos_app/uploads/` |

### **Paso 10: Reload y Probar**

1. **Click "Reload"** (botón verde)
2. **Visitar**: `http://metadatos.pythonanywhere.com/`
3. **Probar login** en `/login` con las credenciales del .env
4. **Subir archivo de prueba** para verificar funcionalidad

---

## 🐳 **Containerización con Podman**

### **Prerrequisitos**
- Podman instalado en tu sistema
- Proyecto Metadatos App funcionando localmente

### **Paso 1: Instalar Podman**

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install podman
```

**macOS:**
```bash
brew install podman
```

**Fedora/CentOS:**
```bash
sudo dnf install podman
```

### **Paso 2: Preparar Archivos de Container**

#### **Crear Dockerfile:**
```dockerfile
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    FLASK_ENV=production

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

# Copiar código de la aplicación
COPY . .

# Crear directorios con permisos
RUN mkdir -p uploads logs data static/uploads && \
    chmod -R 777 uploads logs data static && \
    touch logs/app.log && \
    chmod 666 logs/app.log

EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "wsgi:application"]
```

#### **Crear .dockerignore:**
```dockerignore
# Git
.git
.gitignore

# Python
__pycache__/
*.pyc
venv/
env/

# Local development
.env.local
uploads/
logs/
*.log
*.db
*.sqlite*

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Documentation
README.md
docs/
```

#### **Crear docker-compose.yml:**
```yaml
version: '3.8'

services:
  metadatos-app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: metadatos-app
    restart: unless-stopped

    environment:
      - SECRET_KEY=${SECRET_KEY:-change-this-secret-key-in-production}
      - FLASK_ENV=production
      - FLASK_DEBUG=False
      - DATABASE_URL=sqlite:///data/metadatos.db
      - ADMIN_USERNAME=${ADMIN_USERNAME:-admin}
      - ADMIN_PASSWORD=${ADMIN_PASSWORD:-change-this-password}
      - UPLOAD_FOLDER=uploads
      - MAX_CONTENT_LENGTH=16777216
      - LOG_LEVEL=INFO
      - BASE_URL=http://localhost:5000

    ports:
      - "5000:5000"

    volumes:
      - metadatos_data:/app/data
      - metadatos_uploads:/app/uploads
      - metadatos_logs:/app/logs

    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

volumes:
  metadatos_data:
  metadatos_uploads:
  metadatos_logs:
```

### **Paso 3: Agregar Health Check**

Agregar esta ruta al archivo `app.py`:

```python
@app.route('/health')
def health_check():
    """Health check endpoint for Docker"""
    try:
        # Verificar base de datos
        db.session.execute(db.text('SELECT 1'))
        return {'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}, 200
    except Exception as e:
        return {'status': 'unhealthy', 'error': str(e)}, 500
```

### **Paso 4: Crear Variables de Entorno para Container**

```bash
# Crear archivo .env.docker
cat > .env.docker << 'EOF'
SECRET_KEY=docker-secret-key-change-in-production-2024
ADMIN_USERNAME=admin_docker
ADMIN_PASSWORD=DockerPassword2024!
DATABASE_URL=sqlite:///data/metadatos.db
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
BASE_URL=http://localhost:5000
DC_CREATOR=Metadatos App Docker
DC_PUBLISHER=Metadatos App
DC_RIGHTS=© 2024 Metadatos App Docker. Todos los derechos reservados.
DC_LANGUAGE=es
FLASK_ENV=production
FLASK_DEBUG=False
EOF
```

### **Paso 5: Construir y Ejecutar con Podman**

#### **Opción A: Contenedor Simple**

```bash
# Construir la imagen
podman build -t metadatos-app:latest .

# Verificar que se creó
podman images

# Ejecutar el contenedor
podman run -d \
  --name metadatos-app \
  -p 5000:5000 \
  --env-file .env.docker \
  -v metadatos_data:/app/data \
  -v metadatos_uploads:/app/uploads \
  -v metadatos_logs:/app/logs \
  metadatos-app:latest

# Verificar que está corriendo
podman ps

# Ver logs
podman logs metadatos-app
```

#### **Opción B: Docker Compose con Podman**

```bash
# Instalar podman-compose (si no lo tienes)
pip install podman-compose

# Ejecutar con compose
podman-compose up -d

# Ver estado
podman-compose ps

# Ver logs
podman-compose logs -f metadatos-app

# Parar servicios
podman-compose down
```

### **Paso 6: Verificar la Aplicación**

1. **Abrir navegador** en: `http://localhost:5000`
2. **Probar login** con credenciales del .env.docker:
   - Usuario: `admin_docker`
   - Contraseña: `DockerPassword2024!`
3. **Subir archivo de prueba** para verificar persistencia

### **Paso 7: Comandos Útiles de Podman**

```bash
# Ver contenedores corriendo
podman ps

# Ver logs en tiempo real
podman logs -f metadatos-app

# Entrar al contenedor
podman exec -it metadatos-app /bin/bash

# Ver uso de recursos
podman stats metadatos-app

# Parar contenedor
podman stop metadatos-app

# Reiniciar contenedor
podman restart metadatos-app

# Eliminar contenedor
podman rm metadatos-app

# Eliminar imagen
podman rmi metadatos-app:latest
```

### **Paso 8: Actualizar la Aplicación**

```bash
# Para actualizar después de cambios en el código:

# Parar y eliminar contenedor
podman stop metadatos-app && podman rm metadatos-app

# Reconstruir imagen
podman build -t metadatos-app:latest .

# Ejecutar nuevo contenedor
podman run -d \
  --name metadatos-app \
  -p 5000:5000 \
  --env-file .env.docker \
  -v metadatos_data:/app/data \
  -v metadatos_uploads:/app/uploads \
  -v metadatos_logs:/app/logs \
  metadatos-app:latest
```

---

## 🔧 **Configuración Avanzada**

### **Variables de Entorno Disponibles**

| Variable | Descripción | Valor por Defecto |
|----------|-------------|-------------------|
| `SECRET_KEY` | Clave secreta de Flask (OBLIGATORIO) | - |
| `ADMIN_USERNAME` | Usuario administrador | `admin` |
| `ADMIN_PASSWORD` | Contraseña administrador | `adminpass123!` |
| `DATABASE_URL` | URL de conexión a BD | `sqlite:///metadatos.db` |
| `UPLOAD_FOLDER` | Carpeta de archivos | `uploads` |
| `MAX_CONTENT_LENGTH` | Tamaño máximo archivo | `16777216` (16MB) |
| `LOG_LEVEL` | Nivel de logging | `INFO` |
| `LOG_FILE` | Archivo de logs | `app.log` |

### **Tipos de Archivo Soportados**

#### 📄 **Documentos**
- PDF, DOC, DOCX, TXT, RTF, ODT
- XLS, XLSX, CSV, ODS
- PPT, PPTX, ODP

#### 🖼️ **Imágenes**
- JPG, JPEG, PNG, GIF
- BMP, WEBP, SVG

#### 🎵 **Multimedia**
- MP3, WAV, OGG (Audio)
- MP4, AVI, MKV, MOV (Video)

#### 📦 **Archivos Comprimidos**
- ZIP, RAR, 7Z
- TAR, GZ

#### 💾 **Datos**
- JSON, XML
- Archivos de configuración

---

## 📖 **Guía de Usuario**

### **Para Usuarios Públicos**

1. **Explorar Archivos:**
   - Visita la página principal
   - Navega por las tarjetas de archivos
   - Usa el buscador para encontrar contenido específico

2. **Ver Detalles:**
   - Haz clic en "Ver Detalles" para información completa
   - Visualiza metadatos Dublin Core
   - Descarga archivos directamente

3. **Búsqueda:**
   - Busca por título, descripción o palabras clave
   - Utiliza filtros por tipo de archivo
   - Navega por páginas de resultados

### **Para Administradores**

1. **Acceso:**
   - Ve a `/login`
   - Ingresa credenciales de administrador
   - Accede al panel de control

2. **Subir Archivos:**
   - Completa título y descripción
   - Selecciona archivo (máx. 16MB)
   - Agrega palabras clave opcionales
   - Confirma la subida

3. **Gestionar Archivos:**
   - Ver lista completa con paginación
   - Eliminar archivos con confirmación
   - Monitorear actividad en logs

---

## 🔍 **Solución de Problemas**

### **Problemas Comunes**

#### **Error: "Secret key not configured"**
```bash
# Verificar que SECRET_KEY esté configurada
echo $SECRET_KEY

# Si está vacía, configurarla:
export SECRET_KEY="tu-clave-secreta-aqui"
```

#### **Error: "Permission denied" en uploads**
```bash
# Dar permisos a la carpeta uploads
chmod 755 uploads/
chown -R www-data:www-data uploads/  # En producción
```

#### **Error: "Database not found"**
```bash
# Inicializar base de datos
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

#### **Archivos no se muestran**
- Verificar permisos de la carpeta `uploads/`
- Confirmar que la ruta en `.env` sea correcta
- Revisar logs para errores específicos

#### **Problemas con Podman**
```bash
# Ver logs detallados del contenedor
podman logs metadatos-app

# Verificar puertos
podman port metadatos-app

# Entrar al contenedor para debug
podman exec -it metadatos-app /bin/bash

# Verificar volúmenes
podman inspect metadatos-app
```

### **Debugging**

```bash
# Activar modo debug (solo desarrollo)
export FLASK_DEBUG=True
flask run

# Ver logs en tiempo real
tail -f app.log

# Verificar configuración
python -c "from app import app; print(app.config)"

# Para containers
podman logs -f metadatos-app
```

---

## 📚 **Recursos Adicionales**

### **Documentación**
- [Dublin Core Metadata Initiative](https://www.dublincore.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.3/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Podman Documentation](https://podman.io/docs)
- [PythonAnywhere Help](https://help.pythonanywhere.com/)

---

## 👥 **Equipo y Contacto**

**Desarrollador Principal:** Gabriel Araya
**GitHub:** [@Gabo-araya](https://github.com/Gabo-araya)
**LinkedIn:** [Gabriel Araya](https://www.linkedin.com/in/gaboaraya/)

---

## 🙏 **Agradecimientos**

- **Flask Team** - Por el excelente framework
- **Bootstrap Team** - Por los componentes UI
- **Dublin Core Initiative** - Por los estándares de metadatos
- **Font Awesome & Bootstrap Icons** - Por la iconografía
- **PythonAnywhere** - Por la plataforma de hosting
- **Podman Community** - Por la tecnología de containers
- **Comunidad Open Source** - Por las contribuciones y feedback

---
