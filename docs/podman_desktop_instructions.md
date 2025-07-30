# 🐳 **PARTE 2: Containerización con Podman Desktop**

## 📋 **Requisitos Previos**
- ✅ Proyecto Metadatos App funcionando localmente
- ✅ Podman Desktop instalado

---

## 🚀 **Paso 1: Instalar Podman Desktop**

### **Windows:**
1. **Descargar** desde [podman-desktop.io](https://podman-desktop.io/)
2. **Ejecutar** el instalador `.exe`
3. **Seguir** el asistente de instalación
4. **Reiniciar** si es necesario

### **macOS:**
1. **Descargar** desde [podman-desktop.io](https://podman-desktop.io/)
2. **Arrastrar** la aplicación a la carpeta Applications
3. **Abrir** Podman Desktop desde Launchpad

### **Linux (Ubuntu/Debian):**
```bash
# Opción 1: Descargar desde la web
wget https://github.com/containers/podman-desktop/releases/latest/download/podman-desktop-*.deb
sudo dpkg -i podman-desktop-*.deb

# Opción 2: Flatpak
flatpak install flathub io.podman_desktop.PodmanDesktop
```

## 🔧 **Paso 2: Configurar Podman Desktop**

1. **Abrir Podman Desktop**
2. **Primera configuración**:
   - Click en "Initialize and start" si aparece
   - Esperar a que se inicialice Podman
   - Verificar que aparezca "Podman is running" ✅

3. **Verificar configuración**:
   - Ir a **Settings** → **Resources**
   - Verificar que Podman esté corriendo
   - Anotar la información de conexión

### **Instalar Podman** (si no lo tienes)

**En Ubuntu/Debian**:
```bash
sudo apt update
sudo apt install podman
```

**En CentOS/RHEL/Fedora**:
```bash
sudo dnf install podman
```

**En macOS**:
```bash
brew install podman
```

## 📁 **Paso 3: Preparar el Proyecto**

1. **Abrir terminal/command prompt** en el directorio del proyecto
2. **Crear los archivos necesarios** (usar los artifacts anteriores)


### **Artifact: Crear Dockerfile**
En el directorio raíz del proyecto, crear `Dockerfile`:

```
# Metadatos App - Dockerfile
FROM python:3.10-slim

# Metadata
LABEL maintainer="Metadatos App Team"
LABEL description="Metadatos App - Flask application with Dublin Core metadata support"
LABEL version="2.0"

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    FLASK_ENV=production

# Crear usuario no-root por seguridad
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

# Copiar código de la aplicación
COPY . .

# Crear directorios necesarios
RUN mkdir -p uploads logs static/uploads && \
    chown -R appuser:appuser /app

# Cambiar a usuario no-root
USER appuser

# Exponer puerto
EXPOSE 5000

# Comando de salud
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Comando por defecto
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "wsgi:application"]
```

### **Artifact: Crear .dockerignore**

```
# Metadatos App - .dockerignore

# Git
.git
.gitignore
.gitattributes

# Documentation
README.md
docs/
*.md

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
.venv/

# Local development
.env.local
.env.development
instance/
uploads/
logs/
*.log
*.db
*.sqlite
*.sqlite3

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Testing
.coverage
.pytest_cache/
.tox/
htmlcov/

# Build artifacts
build/
dist/
*.egg-info/

# Deployment specific
docker-compose.override.yml
Dockerfile.dev
.dockerignore.local
```

### **Artifact: Crear docker-compose.yml**

```
# Metadatos App - Docker Compose Configuration
version: '3.8'

services:
  # Aplicación principal
  metadatos-app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: metadatos-app
    restart: unless-stopped

    # Variables de entorno
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
      - LOG_FILE=logs/app.log
      - BASE_URL=http://localhost:5000

    # Puertos
    ports:
      - "5000:5000"

    # Volúmenes para persistencia
    volumes:
      - metadatos_data:/app/data
      - metadatos_uploads:/app/uploads
      - metadatos_logs:/app/logs

    # Dependencias de salud
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

    # Recursos
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M

  # Nginx como proxy reverso (opcional)
  nginx:
    image: nginx:alpine
    container_name: metadatos-nginx
    restart: unless-stopped

    ports:
      - "80:80"

    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - metadatos_uploads:/var/www/uploads:ro

    depends_on:
      - metadatos-app

    profiles:
      - production

# Volúmenes nombrados para persistencia
volumes:
  metadatos_data:
    driver: local
  metadatos_uploads:
    driver: local
  metadatos_logs:
    driver: local

# Red personalizada
networks:
  default:
    name: metadatos-network
```

### **Artifact: Crear nginx.conf (Opcional para Producción)**

```
# Metadatos App - Nginx Configuration
events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    # Logging
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                   '$status $body_bytes_sent "$http_referer" '
                   '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;
    error_log /var/log/nginx/error.log warn;

    # Basic settings
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    client_max_body_size 20M;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml
        image/svg+xml;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

    # Upstream para la aplicación Flask
    upstream metadatos_app {
        server metadatos-app:5000 fail_timeout=30s max_fails=3;
    }

    server {
        listen 80;
        server_name localhost;

        # Security headers
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        add_header Referrer-Policy "strict-origin-when-cross-origin";

        # Favicon
        location /favicon.ico {
            alias /var/www/uploads/favicon.ico;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }

        # Static files
        location /static/ {
            alias /var/www/static/;
            expires 1y;
            add_header Cache-Control "public, immutable";

            # Gzip static files
            location ~* \.(css|js)$ {
                gzip_static on;
                expires 1y;
            }
        }

        # Uploaded files
        location /uploads/ {
            alias /var/www/uploads/;
            expires 1d;
            add_header Cache-Control "public";

            # Security for uploads
            location ~* \.(php|jsp|asp|sh|py)$ {
                deny all;
            }
        }

        # Rate limiting for sensitive endpoints
        location /login {
            limit_req zone=login burst=3 nodelay;
            proxy_pass http://metadatos_app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /admin {
            limit_req zone=api burst=10 nodelay;
            proxy_pass http://metadatos_app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Main application
        location / {
            proxy_pass http://metadatos_app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            # Timeouts
            proxy_connect_timeout 30s;
            proxy_send_timeout 30s;
            proxy_read_timeout 30s;
        }

        # Health check
        location /health {
            access_log off;
            proxy_pass http://metadatos_app;
            proxy_set_header Host $host;
        }

        # Error pages
        error_page 404 /404.html;
        error_page 500 502 503 504 /50x.html;

        location = /404.html {
            internal;
            proxy_pass http://metadatos_app;
        }

        location = /50x.html {
            internal;
            proxy_pass http://metadatos_app;
        }
    }
}
```

### **Artifact: Agregar Health Check al app.py**


Agregar esta ruta a tu `app.py`:

```python
@app.route('/health')
def health_check():
    """Health check endpoint for Docker"""
    try:
        # Verificar base de datos
        db.session.execute('SELECT 1')
        return {'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}, 200
    except Exception as e:
        return {'status': 'unhealthy', 'error': str(e)}, 500
```

### **Artifact: Construir y Ejecutar con Podman**

```bash
# Crear archivo .env para Docker .env.docker
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
EOF

# Construir la imagen
podman build -t metadatos-app:latest .

# Verificar que se creó
podman images

# Ejecutar el contenedor (modo simple)
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

# Probar la aplicación
curl http://localhost:5000
```

### **Artifact: Usar Docker Compose con Podman**

```bash
# Instalar podman-compose si no lo tienes
pip install podman-compose

# O usar docker-compose con podman
export DOCKER_HOST=unix:///run/user/$UID/podman/podman.sock

# Ejecutar con compose
podman-compose up -d

# Ver estado
podman-compose ps

# Ver logs
podman-compose logs -f metadatos-app

# Parar servicios
podman-compose down
```

### **Artifact: Comandos Útiles de Podman**

```bash
# Ver contenedores corriendo
podman ps

# Ver todas las imágenes
podman images

# Entrar al contenedor
podman exec -it metadatos-app /bin/bash

# Ver logs en tiempo real
podman logs -f metadatos-app

# Parar contenedor
podman stop metadatos-app

# Reiniciar contenedor
podman restart metadatos-app

# Eliminar contenedor
podman rm metadatos-app

# Eliminar imagen
podman rmi metadatos-app:latest

# Ver uso de recursos
podman stats metadatos-app

# Inspeccionar contenedor
podman inspect metadatos-app
```

---

### **Crear Dockerfile:**
```bash
# Crear archivo Dockerfile en la raíz del proyecto
touch Dockerfile
```
**Copiar el contenido del Dockerfile** del artifact anterior.

### **Crear .dockerignore:**
```bash
# Crear archivo .dockerignore
touch .dockerignore
```
**Copiar el contenido del .dockerignore** del artifact anterior.

### **Crear docker-compose.yml:**
```bash
# Crear archivo docker-compose.yml
touch docker-compose.yml
```
**Copiar el contenido del docker-compose.yml** del artifact anterior.

### **Crear archivo .env para Docker:**
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
EOF
```

## 🔨 **Paso 4: Construir la Imagen con Podman Desktop**

### **Opción A: Usando la Interfaz Gráfica**

1. **Abrir Podman Desktop**
2. **Ir a la pestaña "Images"**
3. **Click en "Build"** (botón azul arriba a la derecha)
4. **Configurar el build**:
   - **Containerfile path**: Navegar y seleccionar tu `Dockerfile`
   - **Build context directory**: Seleccionar la carpeta raíz de tu proyecto
   - **Image name**: `metadatos-app`
   - **Tag**: `latest`
5. **Click "Build"**
6. **Esperar** a que termine el proceso (aparecerán los logs)
7. **Verificar** que la imagen aparezca en la lista

### **Opción B: Usando Terminal Integrada**

1. **En Podman Desktop**, ir a **Settings** → **Terminal**
2. **Abrir terminal integrada** o usar tu terminal preferida
3. **Navegar al directorio del proyecto**:
```bash
cd /ruta/a/tu/proyecto/metadatos-app
```

4. **Construir la imagen**:
```bash
podman build -t metadatos-app:latest .
```

5. **Verificar en Podman Desktop**:
   - Ir a la pestaña "Images"
   - Debería aparecer `metadatos-app:latest`

## 🚀 **Paso 5: Crear y Ejecutar Contenedor**

### **Opción A: Usando la Interfaz Gráfica**

1. **En la pestaña "Images"**, encontrar `metadatos-app:latest`
2. **Click en "Run"** (botón play ▶️)
3. **Configurar el contenedor**:

   **Basic Settings:**
   - **Container name**: `metadatos-app-container`
   - **Port mapping**: `5000:5000`

   **Advanced Settings (click en "Advanced"):**
   - **Environment variables** (click "+" para agregar cada una):
     ```
     SECRET_KEY = docker-secret-key-change-in-production-2024
     ADMIN_USERNAME = admin_docker
     ADMIN_PASSWORD = DockerPassword2024!
     DATABASE_URL = sqlite:///data/metadatos.db
     FLASK_ENV = production
     UPLOAD_FOLDER = uploads
     LOG_LEVEL = INFO
     ```

   **Volumes** (click "+" para agregar cada uno):
   - **Host path**: Crear carpeta `metadatos_data` en tu escritorio
     **Container path**: `/app/data`
   - **Host path**: Crear carpeta `metadatos_uploads` en tu escritorio
     **Container path**: `/app/uploads`
   - **Host path**: Crear carpeta `metadatos_logs` en tu escritorio
     **Container path**: `/app/logs`

4. **Click "Start Container"**

### **Opción B: Usando Terminal**

```bash
# Crear directorios locales para volúmenes
mkdir -p ~/metadatos_docker/{data,uploads,logs}

# Ejecutar contenedor
podman run -d \
  --name metadatos-app-container \
  -p 5000:5000 \
  --env-file .env.docker \
  -v ~/metadatos_docker/data:/app/data \
  -v ~/metadatos_docker/uploads:/app/uploads \
  -v ~/metadatos_docker/logs:/app/logs \
  metadatos-app:latest
```

## 📊 **Paso 6: Verificar el Contenedor**

### **En Podman Desktop:**

1. **Ir a la pestaña "Containers"**
2. **Verificar que aparezca** `metadatos-app-container`
3. **Estado debe ser** "Running" con punto verde ✅
4. **Click en el contenedor** para ver detalles

### **Verificar Logs:**
1. **En la vista del contenedor**, click en **"Logs"**
2. **Deberías ver**:
   ```
   ✅ Base de datos inicializada
   🚀 WSGI configurado correctamente para Metadatos App
   [INFO] Starting gunicorn 21.2.0
   [INFO] Listening at: http://0.0.0.0:5000
   ```

### **Probar la Aplicación:**
1. **Abrir navegador**
2. **Ir a**: `http://localhost:5000`
3. **Debería cargar** la página principal de Metadatos App

## 🔧 **Paso 7: Gestionar el Contenedor desde Podman Desktop**

### **Ver Información del Contenedor:**
1. **Click en el contenedor** en la lista
2. **Pestañas disponibles**:
   - **Summary**: Información general
   - **Logs**: Logs en tiempo real
   - **Inspect**: Configuración detallada
   - **Terminal**: Acceso a terminal del contenedor

### **Acceder al Terminal del Contenedor:**
1. **Click en "Terminal"** en la vista del contenedor
2. **Ejecutar comandos dentro del contenedor**:
```bash
# Verificar archivos
ls -la /app

# Ver base de datos
ls -la /app/data

# Ver logs de la aplicación
tail -f /app/logs/app.log

# Verificar Python y dependencias
python --version
pip list
```

### **Controlar el Contenedor:**
- **▶️ Start**: Iniciar contenedor parado
- **⏸️ Stop**: Parar contenedor
- **🔄 Restart**: Reiniciar contenedor
- **🗑️ Delete**: Eliminar contenedor (datos en volúmenes se mantienen)

## 📋 **Paso 8: Probar la Aplicación Completamente**

1. **Página Principal**: `http://localhost:5000`
   - ✅ Debería mostrar "No hay archivos disponibles"

2. **Login de Admin**: `http://localhost:5000/login`
   - **Usuario**: `admin_docker`
   - **Contraseña**: `DockerPassword2024!`
   - ✅ Debería permitir login

3. **Panel de Admin**: `http://localhost:5000/admin`
   - ✅ Subir un archivo de prueba
   - ✅ Verificar que aparece en la lista

4. **Verificar Persistencia**:
   - Parar el contenedor en Podman Desktop
   - Iniciarlo de nuevo
   - ✅ Los archivos subidos deben seguir ahí

## 🐙 **Paso 9: Usar Docker Compose en Podman Desktop**

### **Habilitar Docker Compose:**
1. **En Podman Desktop**, ir a **Settings**
2. **En "Extensions"**, buscar **"Docker Compose"**
3. **Instalar** si no está instalado
4. **Activar** la extensión

### **Ejecutar con Compose:**

1. **Crear archivo docker-compose.override.yml** para desarrollo:
```yaml
# docker-compose.override.yml
version: '3.8'

services:
  metadatos-app:
    ports:
      - "5000:5000"
    environment:
      - FLASK_DEBUG=True
      - LOG_LEVEL=DEBUG
    volumes:
      - ./:/app
      - metadatos_data:/app/data
      - metadatos_uploads:/app/uploads
      - metadatos_logs:/app/logs

volumes:
  metadatos_data:
  metadatos_uploads:
  metadatos_logs:
```

2. **En terminal**:
```bash
# Ejecutar con compose
podman-compose up -d

# Ver logs
podman-compose logs -f

# Parar servicios
podman-compose down
```

3. **En Podman Desktop**:
   - Los servicios de compose aparecerán en "Containers"
   - Se pueden gestionar igual que contenedores individuales

## 🔄 **Paso 10: Actualizar la Aplicación**

### **Cuando hagas cambios al código:**

1. **Reconstruir imagen**:
   - En Podman Desktop → "Images"
   - Click en los 3 puntos de `metadatos-app:latest`
   - "Delete image"
   - Volver a construir con "Build"

2. **O desde terminal**:
```bash
# Parar contenedor
podman stop metadatos-app-container

# Eliminar contenedor
podman rm metadatos-app-container

# Reconstruir imagen
podman build -t metadatos-app:latest .

# Ejecutar nuevo contenedor
podman run -d \
  --name metadatos-app-container \
  -p 5000:5000 \
  --env-file .env.docker \
  -v ~/metadatos_docker/data:/app/data \
  -v ~/metadatos_docker/uploads:/app/uploads \
  -v ~/metadatos_docker/logs:/app/logs \
  metadatos-app:latest
```

## 📊 **Paso 11: Monitoreo y Debugging**

### **Ver Estadísticas de Recursos:**
1. **En Podman Desktop**, ir a la vista del contenedor
2. **Pestaña "Summary"** muestra:
   - CPU usage
   - Memory usage
   - Network I/O
   - Storage usage

### **Debugging Común:**

**Si el contenedor no inicia:**
```bash
# Ver logs detallados
podman logs metadatos-app-container

# Verificar configuración
podman inspect metadatos-app-container
```

**Si no puedes acceder a localhost:5000:**
```bash
# Verificar puertos
podman port metadatos-app-container

# Verificar que el puerto esté libre en tu máquina
netstat -an | grep 5000
```

**Si hay errores de permisos:**
```bash
# Entrar al contenedor y verificar
podman exec -it metadatos-app-container /bin/bash
ls -la /app
whoami
```

## 📤 **Paso 12: Compartir la Imagen (Opcional)**

### **Exportar imagen:**
1. **En Podman Desktop** → "Images"
2. **Click en los 3 puntos** de tu imagen
3. **"Save image"**
4. **Elegir ubicación** y guardar como `.tar`

### **Importar imagen en otra máquina:**
```bash
podman load -i metadatos-app-latest.tar
```


---

## 🔍 **Verificación y Troubleshooting**


1. **Si el contenedor no inicia**:
   ```bash
   podman logs metadatos-app
   ```

2. **Si hay problemas de permisos**:
   ```bash
   podman exec -it metadatos-app ls -la /app
   ```

3. **Si no puede conectar a la aplicación**:
   ```bash
   podman port metadatos-app
   ```
---
