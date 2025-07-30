# 📁 Metadatos App v2.0

Una aplicación web moderna y robusta desarrollada con Flask para la gestión integral de archivos digitales con soporte completo para metadatos Dublin Core. Incluye un panel de administración avanzado, sistema de búsqueda, y una interfaz pública responsive.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
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

## 🌐 **Despliegue en Producción**

### **PythonAnywhere (Recomendado para principiantes)**

1. **Preparar el código:**
```bash
git push origin main  # Asegurar que el código esté en GitHub
```

2. **En PythonAnywhere:**
```bash
# Clonar repositorio
git clone https://github.com/Gabo-araya/metadatos-app.git metadatos_app

# Crear entorno virtual
mkvirtualenv --python=/usr/bin/python3.10 metadatos_env

# Instalar dependencias
cd metadatos_app
pip install -r requirements.txt
```

3. **Configurar aplicación web:**
   - Ve a la pestaña "Web"
   - Crea nueva aplicación Flask
   - Configura el archivo WSGI: `/var/www/tu_usuario_pythonanywhere_com_wsgi.py`

```python
import sys
project_home = '/home/tu_usuario/metadatos_app'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

from wsgi import application
```

4. **Configurar variables de entorno en la pestaña "Files" → `.env`**

### **VPS con Nginx + Gunicorn**

1. **Instalar dependencias del sistema:**
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx supervisor
```

2. **Configurar aplicación:**
```bash
cd /var/www/
sudo git clone https://github.com/Gabo-araya/metadatos-app.git metadatos_app
cd metadatos_app
sudo python3 -m venv venv
sudo venv/bin/pip install -r requirements.txt
sudo venv/bin/pip install gunicorn
```

3. **Configurar Gunicorn (`/etc/supervisor/conf.d/metadatos.conf`):**
```ini
[program:metadatos]
command=/var/www/metadatos_app/venv/bin/gunicorn --workers 3 --bind unix:/var/www/metadatos_app/metadatos.sock -m 007 wsgi:application
directory=/var/www/metadatos_app
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
```

4. **Configurar Nginx (`/etc/nginx/sites-available/metadatos`):**
```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/metadatos_app/metadatos.sock;
    }

    location /static {
        alias /var/www/metadatos_app/static;
    }

    location /uploads {
        alias /var/www/metadatos_app/uploads;
    }
}
```

### **Docker (Avanzado)**

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:application"]
```

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

## 📚 **Recursos Adicionales**

### **Documentación**
- [Dublin Core Metadata Initiative](https://www.dublincore.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.3/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

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
- **Comunidad Open Source** - Por las contribuciones y feedback

---
